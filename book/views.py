from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, FavoriteBook, Review, BookStatus
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import BookSearchForm
import requests
from django.contrib.auth.decorators import login_required

def home(request):
    searchTerm = request.GET.get('searchBook')

    if searchTerm:
        books = Book.objects.filter(title__icontains=searchTerm)
    else:
        books = Book.objects.all()

    favorite_book_ids = []
    book_statuses = {}
    if request.user.is_authenticated:
        favorite_books = FavoriteBook.objects.filter(user=request.user)
        favorite_book_ids = [fav.book.id for fav in favorite_books]

       
        statuses = BookStatus.objects.filter(user=request.user, book__in=books)
        book_statuses = {bs.book.id: bs.status for bs in statuses}

    return render(request, "home.html", {
        "searchTerm": searchTerm,
        "books": books,
        "favorite_book_ids": favorite_book_ids,
        "book_statuses": book_statuses,  
    })


def favorite_books(request):
    if request.user.is_authenticated:
        favorite_books = FavoriteBook.objects.filter(user=request.user)
    else:
        favorite_books = []

    return render(request, 'favorite_books.html', {
        'favorite_books': favorite_books,
    })



def book_reviews(request, book_id):
    
    book = get_object_or_404(Book, id=book_id)
    
   
    reviews = Review.objects.filter(book=book).select_related('user')  

    return render(request, 'book_reviews.html', {
        'book': book,
        'reviews': reviews,
    })

@require_POST
def delete_review(request, review_id):
    print(f"Attempting to delete review with ID: {review_id}")  
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'unauthenticated'}, status=401)

@require_POST
def add_review(request, book_id):
    if request.user.is_authenticated:
        content = request.POST.get('content')
        book = get_object_or_404(Book, id=book_id)
        if content:
            Review.objects.create(user=request.user, book=book, content=content)
        return redirect('book_reviews', book_id=book.id)  
    return redirect('login')

@require_POST
def toggle_favorite(request, book_id):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(id=book_id)
            favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)
            if not created:
                favorite.delete()
                return JsonResponse({'status': 'removed'})
            return JsonResponse({'status': 'added'})
        except Book.DoesNotExist:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'unauthenticated'}, status=401)

def check_open_library_availability(book_title):
    search_url = f"https://openlibrary.org/search.json?q={book_title.replace(' ', '+')}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        if 'docs' in data and data['docs']:
            book = data['docs'][0]

            return {
                'title': book.get('title', 'No title'),
                'authors': book.get('author_name', ['Desconocido']),
                'year': book.get('first_publish_year'),
                'availability': 'Disponible para préstamo' if 'key' in book else 'Sin información',
                'url': f"https://openlibrary.org{book.get('key')}" if book.get('key') else None,
                'image_url': f"https://covers.openlibrary.org/b/id/{book.get('cover_i')}-L.jpg" if book.get('cover_i') else None,
                'synopsis': book.get('first_sentence', [''])[0] if isinstance(book.get('first_sentence'), list) else book.get('first_sentence')
            }
        else:
            return None
    else:
        return None


def book_search(request):
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data['book_name']
            availability_data = check_open_library_availability(book_name)

            if availability_data:
                return render(request, 'book_search.html', {
                    'form': form,
                    'availability_data': availability_data
                })
            else:
                return render(request, 'book_search.html', {
                    'form': form,
                    'availability_info': 'No se encontraron resultados.'
                })
    else:
        form = BookSearchForm()

    return render(request, 'book_search.html', {'form': form})


@login_required
@require_POST
def set_book_status(request, book_id):
    status = request.POST.get('status')
    if status not in ['to_read', 'reading', 'read']:
        return JsonResponse({'status': 'invalid_status'}, status=400)

    book = get_object_or_404(Book, id=book_id)
    BookStatus.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={'status': status}
    )
    return JsonResponse({'status': 'ok'})


@login_required
def book_status_list(request):
    statuses = BookStatus.objects.filter(user=request.user).select_related('book')
    books_by_status = {
        'to_read': [],
        'reading': [],
        'read': [],
    }

    for bs in statuses:
        books_by_status[bs.status].append(bs.book)

    return render(request, 'book_status_list.html', {
        'books_by_status': books_by_status
    })
