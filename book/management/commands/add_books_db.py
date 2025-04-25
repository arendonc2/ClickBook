from django.core.management.base import BaseCommand
from book.models import Book
import json

class Command(BaseCommand):
    help = 'Load books from book_descriptions.json into the Book model'
    
    def handle(self, *args, **kwargs):
        json_file_path = 'book/management/commands/books.json'
        
        with open(json_file_path, 'r') as file:
            books = json.load(file)

        for i in range(200):
            book = books[i]
            exist = Book.objects.filter(title=book['title']).first()
            if not exist:
                Book.objects.create(
                    title=book['title'],
                    image='book/images/default_nia.jpg',
                    genre=book['genre'],
                    synopsis=book['synopsis']
                )
                     