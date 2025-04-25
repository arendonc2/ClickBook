from django.shortcuts import render
import requests

def recommendations(request):
    return render(request, 'recommendations.html')

def recommendationsBooks(request):
    return render(request, 'recommendationsBooks.html')

def search_books(request):
    books = []
    if request.method == 'POST':
        query = request.POST['query']
        url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            books = data.get('items', [])
    return render(request, 'search_books.html', {'books': books})

def survey(request):
    if request.method == 'POST':
        # Collect user preferences from the survey
        genre = request.POST.get('genre')
        readings_size = request.POST.get('readings_size')
        favorite_authors = request.POST.getlist('favorite_authors')
        fiction_type = request.POST.get('fiction_type')
        recent_books = request.POST.get('recent_books')

        # Here you would implement your recommendation logic
        recommended_books = recommend_books(genre, favorite_authors, recent_books)

        return render(request, 'recommendationsBooks.html', {'recommended_books': recommended_books})

    return render(request, 'survey.html')

def recommend_books(genre, favorite_authors, recent_books):
    # Placeholder for book recommendation logic
    # You can replace this with actual logic to fetch books based on user preferences
    recommended_books = []

    # Example logic: Fetch books from Google Books API based on genre
    if genre:
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            for item in items:
                book_info = {
                    'title': item['volumeInfo'].get('title'),
                    'authors': item['volumeInfo'].get('authors', []),
                    'description': item['volumeInfo'].get('description', 'No description available.'),
                    'link': item['volumeInfo'].get('infoLink')
                }
                recommended_books.append(book_info)

    return recommended_books


