import os
import numpy as np
from django.core.management.base import BaseCommand
from book.models import Book
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate and store embeddings for all books in the database"

    def handle(self, *args, **kwargs):
 
        load_dotenv('.env')
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

        books = Book.objects.all()
        self.stdout.write(f"Found {books.count()} books in the database")

        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        for book in books:
            try:
                emb = get_embedding(book.synopsis)
           
                book.emb = emb.tobytes()
                book.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Embedding stored for: {book.title}"))
            except Exception as e:
                self.stderr.write(f"❌ Failed to generate embedding for {book.title}: {e}")

        self.stdout.write(self.style.SUCCESS("🎯 Finished generating embeddings for all movies"))
