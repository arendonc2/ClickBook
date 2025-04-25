import os
import re
import requests
from unidecode import unidecode
from openai import OpenAI
from django.core.management.base import BaseCommand
from book.models import Book
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Genera imágenes con OpenAI y actualiza el campo image de los libros"

    def handle(self, *args, **kwargs):
        load_dotenv('.env')


        client = OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
        )

        images_folder = 'media/book/images/'
        os.makedirs(images_folder, exist_ok=True)

   
        books = Book.objects.all()[:100]
        self.stdout.write(f"📚 Se procesarán {books.count()} libros.")

        for book in books:
            try:
    
                cleaned_title = self.clean_filename(book.title)
                image_filename = f"m_{cleaned_title}.png"
                image_full_path = os.path.join(images_folder, image_filename)

 
                self.generate_and_download_image(client, book.title, image_full_path)
            
                book.image = os.path.join('book/images', image_filename)
                book.save()
                self.stdout.write(self.style.SUCCESS(f" Imagen guardada para: {book.title}"))

            except Exception as e:
                default_image_path = os.path.join('book/images', 'censored.png')
                book.image = default_image_path
                book.save()
                self.stdout.write(self.style.WARNING(f" Imagen de censura guardada para: {book.title}"))

        self.stdout.write(self.style.SUCCESS(" Proceso completado."))

    def generate_and_download_image(self, client, book_title, image_full_path):
        """
        Genera una imagen con DALL·E y la guarda localmente.
        Devuelve la ruta relativa para la base de datos.
        """
        prompt = f"Book poster of {book_title}"

    
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

 
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        with open(image_full_path, 'wb') as f:
            f.write(image_response.content)

        return image_full_path

    def clean_filename(self, title):
        """
        Limpia el título del libro para que sea un nombre de archivo válido.
        """
        title = unidecode(title)  
        title = re.sub(r'[<>:"/\\|?*]', '', title) 
        title = re.sub(r'\s+', '_', title).strip()  
        return title[:100] 
