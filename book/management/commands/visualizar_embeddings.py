import os
import numpy as np
import random
from django.core.management.base import BaseCommand
from book.models import Book
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Selecciona un libro al azar y muestra sus embeddings"

    def handle(self, *args, **kwargs):
      
        books_with_emb = Book.objects.exclude(emb__isnull=True).exclude(emb=b'')
        
        if not books_with_emb.exists():
            self.stderr.write("❌ No hay libros con embeddings almacenados.")
            return
        
       
        book = random.choice(books_with_emb)
        
     
        emb_array = np.frombuffer(book.emb, dtype=np.float32)
        
      
        self.stdout.write(self.style.SUCCESS(f"📘 Libro seleccionado: {book.title}"))
        self.stdout.write(f"📏 Tamaño del embedding: {len(emb_array)}")
        self.stdout.write(f"🔢 Primeros 10 valores del embedding: {emb_array[:10]}")
