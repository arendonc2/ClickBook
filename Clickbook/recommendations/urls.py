from django.urls import path
from .views import search_books, survey, recommendationsBooks

from . import views

urlpatterns = [
    path('search/', search_books, name='search_books'),
    path('survey/', survey, name='survey'),
    path('recommendationsBooks/', recommendationsBooks, name='recommendationsBooks'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
