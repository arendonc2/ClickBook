from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    synopsis = models.CharField(max_length=500)
    image = models.ImageField(upload_to='book/image/')
    url = models.URLField(blank=True)