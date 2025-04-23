from django.urls import path
from .views import nearby_libraries, home, favorite_books, toggle_favorite, book_reviews, add_review, delete_review

urlpatterns = [
    path('', home, name='home'),
    path('favorites/', favorite_books, name='favorite_books'),
    path('toggle_favorite/<int:book_id>/', toggle_favorite, name='toggle_favorite'),
    path('nearby-libraries/', nearby_libraries, name='nearby_libraries'),
    path('book/<int:book_id>/reviews/', book_reviews, name='book_reviews'),
    path('book/<int:book_id>/add_review/', add_review, name='add_review'),
    path('review/<int:review_id>/delete/', delete_review, name='delete_review'),
]
