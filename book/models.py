from django.db import models

class Book(models.Model):
    title= models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    image= models.ImageField(upload_to='book/images/')
    genre=models.CharField(max_length=100)
    synopsis= models.CharField(max_length=250)
    url= models.URLField(blank=True)
# Create your models here.
