from django.shortcuts import render
from .models import Book

def home(request):
    searchTerm = request.GET.get('searchBook')

    if searchTerm:
        books = Book.objects.filter(title__icontains=searchTerm)
    else:
        books = Book.objects.all()

    return render(request, "home.html", {"searchTerm": searchTerm, "books": books})


