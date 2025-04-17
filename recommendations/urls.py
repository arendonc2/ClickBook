from django.urls import path
from .views import rate_book, survey, recommendationsBooks


urlpatterns = [
    path('survey/', survey, name='survey'),
    path('recommendationsBooks/', recommendationsBooks, name='recommendationsBooks'),
    path('rate_book/', rate_book, name='rate_book'),
]
