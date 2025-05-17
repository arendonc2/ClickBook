from django.urls import path
from .views import Book_Recommendation, survey, recommendationsBooks, history_of_recommendations, shared_recommendations


urlpatterns = [
    path('survey/', survey, name='survey'),
    path('recommendationsBooks/', recommendationsBooks, name='recommendationsBooks'),
    path('Book_Recommendation/', Book_Recommendation, name='Book_Recommendation'),
    path('history_of_recomedations/', history_of_recommendations, name='history_of_recommendations'),
    path('shared/', shared_recommendations, name='shared_recommendations'),
]
