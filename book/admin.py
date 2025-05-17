from django.contrib import admin
from .models import Book, FavoriteBook,Review,BookStatus

admin.site.register(Book)
admin.site.register(FavoriteBook)
admin.site.register(Review)
admin.site.register(BookStatus)