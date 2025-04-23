from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, FavoriteBook, Review
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.shortcuts import render
from .models import Book

def home(request):
    searchTerm = request.GET.get('searchBook')

    if searchTerm:
        books = Book.objects.filter(title__icontains=searchTerm)
    else:
        books = Book.objects.all()

    favorite_book_ids = []
    if request.user.is_authenticated:
        favorite_books = FavoriteBook.objects.filter(user=request.user)
        favorite_book_ids = [fav.book.id for fav in favorite_books]

    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'books': books,
        'favorite_book_ids': favorite_book_ids,
    })


def nearby_libraries(request):
    return render(request, 'nearby_libraries.html')

def favorite_books(request):
    if request.user.is_authenticated:
        favorite_books = FavoriteBook.objects.filter(user=request.user)
    else:
        favorite_books = []

    return render(request, 'favorite_books.html', {
        'favorite_books': favorite_books,
    })



def book_reviews(request, book_id):
    # Get the book object or return a 404 if it doesn't exist
    book = get_object_or_404(Book, id=book_id)
    
    # Retrieve reviews for the book
    reviews = Review.objects.filter(book=book).select_related('user')  # Assuming you want to show user info

    return render(request, 'book_reviews.html', {
        'book': book,
        'reviews': reviews,
    })

@require_POST
def delete_review(request, review_id):
    print(f"Attempting to delete review with ID: {review_id}")  # Debugging line
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
        return redirect('book_reviews', book_id=book.id)  # <- nombre correcto
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