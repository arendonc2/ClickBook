from django.db import models
from django.contrib.auth.models import User
from book.models import Book  

class BookRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  

    def __str__(self): 
        return self.book.title 


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferred_genres = models.CharField(max_length=100)
    favorite_authors = models.TextField()
    preferred_length = models.CharField(max_length=100)
    preferred_era = models.CharField(max_length=50)
    liked_books = models.TextField()

    def __str__(self):
        return f"Preferencias de {self.user.username}"
