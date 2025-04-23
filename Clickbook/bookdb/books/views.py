# books/views.py
import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = load_users()
        if username not in users:
            users[username] = password
            save_users(users)
            return redirect('login')
        else:
            return HttpResponse("User  already exists.")
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = load_users()
        if username in users and users[username] == password:
            request.session['username'] = username
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials.")
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()  # Clear the session
    return redirect('home')  # Redirect to the home page after logout

def home(request):
    username = request.session.get('username')
    return render(request, 'home.html', {'username': username})

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

        return render(request, 'recommendations.html', {'recommended_books': recommended_books})

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
