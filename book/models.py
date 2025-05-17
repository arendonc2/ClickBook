from django.db import models
from django.contrib.auth.models import User
import numpy as np

def get_default_array():
    default_arr = np.random.rand(1536)
    return default_arr.tobytes()


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='book_images/', default='book_images/default_nia.jpg', blank=True, null=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
    synopsis = models.TextField(blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    emb = models.BinaryField(default=get_default_array())
    
    def __str__(self): 
        return self.title
    
class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"
    

class BookStatus(models.Model):
    STATUS_CHOICES = [
        ('to_read', 'To read'), # Por leer
        ('reading', 'Reading'),  # Leyendo 
        ('read', 'Read'),  # Leído
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'book')  # Evita duplicados

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"


