from django.urls import path
from .views import  home, favorite_books, toggle_favorite, book_reviews, add_review, delete_review, book_search,set_book_status,book_status_list 


urlpatterns = [
    path('', home, name='home'),
    path('favorites/', favorite_books, name='favorite_books'),
    path('toggle_favorite/<int:book_id>/', toggle_favorite, name='toggle_favorite'),
    path('book/<int:book_id>/reviews/', book_reviews, name='book_reviews'),
    path('book/<int:book_id>/add_review/', add_review, name='add_review'),
    path('review/<int:review_id>/delete/', delete_review, name='delete_review'),
    path('book_search/', book_search, name='book_search'),
    path('set-status/<int:book_id>/', set_book_status, name='set_book_status'),
    path('book-status/', book_status_list, name='book_status_list'),
]


