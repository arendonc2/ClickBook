from django.urls import path
from .views import Book_Recommendation, survey, recommendationsBooks


urlpatterns = [
    path('survey/', survey, name='survey'),
    path('recommendationsBooks/', recommendationsBooks, name='recommendationsBooks'),
    path('Book_Recommendation/', Book_Recommendation, name='Book_Recommendation'),
]
