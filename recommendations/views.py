import base64
import json
from django.shortcuts import render
from openai import OpenAI
import os
import numpy as np
from dotenv import load_dotenv
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import BookRecommendation,Book, UserPreference
import traceback
from .models import UserPreference
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlencode


load_dotenv('.env')
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def recommendationsBooks(request):
    return render(request, 'recommendationsBooks.html')

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_openai_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    embedding = np.array(response.data[0].embedding, dtype=np.float32)
    
 
    print(f"Longitud del embedding del usuario: {embedding.shape[0]}")
    
    return embedding


def survey(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        readings_size = request.POST.get('readings_size')
        favorite_authors = [author.strip() for author in request.POST.get('favorite_authors', '').split(',')]
        fiction_type = request.POST.get('fiction_type')
        recent_books = [book.strip() for book in request.POST.get('recent_books', '').split(',')]

        user_profile_text = (
            f"The user prefers the genre {genre}, enjoys {fiction_type} fiction, "
            f"and usually reads {readings_size.replace('_', ' ')}. "
            f"Their favorite authors include {', '.join(favorite_authors)}. "
            f"Recently enjoyed books: {', '.join(recent_books)}."
        )

        print(f"User profile text: {user_profile_text}")

        try:
            user_embedding = get_openai_embedding(user_profile_text)

            if request.user.is_authenticated:
                UserPreference.objects.create(
                    user=request.user,
                    preferred_genres=genre,
                    preferred_length=readings_size,
                    favorite_authors=', '.join(favorite_authors),
                    preferred_era=fiction_type,
                    liked_books=', '.join(recent_books),
                )
                print("✅ Preferencias guardadas")

            books = Book.objects.all()[:200]
            recommendations = []

            for book in books:
                try:
                    book_embedding = np.frombuffer(book.emb, dtype=np.float32)
                    if book_embedding.shape[0] != user_embedding.shape[0]:
                        print(f"Dimensión incompatible en el libro '{book.title}': {book_embedding.shape[0]}")
                        continue

                    similarity = cosine_similarity(user_embedding, book_embedding)
                    recommendations.append((book, similarity))

                except Exception as e:
                    print(f"Error al procesar el libro '{book.title}': {e}")

            recommendations.sort(key=lambda x: x[1], reverse=True)
            top_recommendations = recommendations[:12]

           
            ids = [str(book.id) for book, _ in top_recommendations]
            encoded = base64.urlsafe_b64encode(json.dumps(ids).encode()).decode()
            share_url = request.build_absolute_uri(reverse('shared_recommendations')) + '?' + urlencode({'data': encoded})

            
            return render(request, 'recommendationsBooks.html', {
                'top_recommendations': top_recommendations,
                'share_url': share_url
            })

        except Exception as e:
            print("❌ Error al generar el embedding del usuario:")
            traceback.print_exc()

    return render(request, 'survey.html')


@login_required
def Book_Recommendation(request):
    if request.method == 'POST':
        try:
            book_id = request.POST.get('book_id')
            rating_value = request.POST.get('rating')

            if not book_id:
                return HttpResponseBadRequest("ID del libro no proporcionado.")

            book = Book.objects.get(id=book_id)

           
            try:
                rating_value = int(rating_value)
            except (ValueError, TypeError):
                rating_value = 0

            BookRecommendation.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'rating': rating_value}
            )

            return redirect('recommendationsBooks')

        except Exception as e:
            print("Error al guardar calificación:", e)
            return HttpResponseBadRequest("Error al guardar calificación")

    return HttpResponseBadRequest("Método no permitido")



@login_required
def history_of_recommendations(request):
    recommendations = BookRecommendation.objects.filter(user=request.user).select_related('book')

    return render(request, 'history_of_recommendations.html', {
        'recommendations': recommendations})


def shared_recommendations(request):
    data = request.GET.get('data')
    if not data:
        return HttpResponseBadRequest("No data provided.")

    try:
        decoded = base64.urlsafe_b64decode(data.encode()).decode()
        ids = json.loads(decoded)
        books = Book.objects.filter(id__in=ids)

       
        return render(request, 'recommendationsBooks.html', {
            'top_recommendations': [(book, 1.0) for book in books],  
            'shared': True
        })

    except Exception as e:
        print("❌ Error al procesar enlace compartido:", e)
        return HttpResponse("Invalid or corrupted link.")
