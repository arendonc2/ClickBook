import os
from openai import OpenAI
from django.core.management.base import BaseCommand
from book.models import Book
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Update book descriptions using OpenAI API"

    def handle(self, *args, **kwargs):
        load_dotenv('.env')

    
        client = OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
        )


        def get_completion(prompt, model="gpt-3.5-turbo"):
            messages = [{"role": "user", "content": prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
            )
            return response.choices[0].message.content.strip()

   
        instruction = (
            "Vas a actuar como un aficionado del cine que sabe describir de forma clara, "
            "concisa y precisa cualquier libro en menos de 200 palabras. La descripción "
            "debe incluir el género del libro y cualquier información adicional que sirva "
            "para crear un sistema de recomendación."
        )

        books = Book.objects.all()
        self.stdout.write(f" Se procesarán {books.count()} libros.")

        for book in books:
            try:
                prompt = (
                    f"{instruction} "
                    f"Vas a actualizar la descripción '{book.synopsis}' del libro '{book.title}'."
                )

                updated_description = get_completion(prompt)

                book.synopsis = updated_description
                book.save()

     
                self.stdout.write(self.style.SUCCESS(f" Descripción generada para: {book.title}"))

            except Exception as e:
                self.stderr.write(f" Falló con {book.title}: {str(e)}")
