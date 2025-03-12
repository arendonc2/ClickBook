# books/views.py
import json
import requests
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


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
<<<<<<< Updated upstream
        fiction_type = request.POST.get('fiction_type')
        recent_books = request.POST.get('recent_books')
=======
        recent_books = request.POST.get('recent_books', '').split(',')
>>>>>>> Stashed changes

        # Get recommended books based on user preferences
        recommended_books = recommend_books(genre, favorite_authors, recent_books)

        return render(request, 'recommendations.html', {'recommended_books': recommended_books})

    return render(request, 'survey.html')

def fetch_books(genre):
    """Fetch books from Google Books API based on genre."""
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def create_book_dataframe(books):
    """Create a DataFrame from the list of books."""
    book_data = []
    for item in books:
        book_info = {
            'title': item['volumeInfo'].get('title'),
            'authors': ', '.join(item['volumeInfo'].get('authors', [])),
            'description': item['volumeInfo'].get('description', 'No description available.'),
            'link': item['volumeInfo'].get('infoLink')
        }
        book_data.append(book_info)
    return pd.DataFrame(book_data)

def recommend_books(genre, favorite_authors, recent_books):
    # Fetch books based on genre
    books = fetch_books(genre)
    if not books:
        return []

    # Create a DataFrame from the fetched books
    book_df = create_book_dataframe(books)

    # Combine favorite authors and recent books into a single string for better recommendations
    user_profile = ' '.join(favorite_authors) + ' ' + ' '.join(recent_books)

    # Create a TF-IDF Vectorizer and fit it on the book descriptions
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(book_df['description'])

    # Calculate the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Get the index of the user's profile (using a dummy book for the profile)
    user_profile_vector = tfidf.transform([user_profile])
    sim_scores = linear_kernel(user_profile_vector, tfidf_matrix).flatten()

    # Get the indices of the top 10 most similar books
    recommended_indices = sim_scores.argsort()[-10:][::-1]

    # Create a list of recommended books with explanations
    recommended_books = []
    for idx in recommended_indices:
        book_info = book_df.iloc[idx].to_dict()
        explanation = f"You liked {genre} and {', '.join(favorite_authors)}. I recommend '{book_info['title']}' because it features themes of {genre} and has elements similar to your recent reads."
        book_info['explanation'] = explanation
        recommended_books.append(book_info)

    return recommended_books


