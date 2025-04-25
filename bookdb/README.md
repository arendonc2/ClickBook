# ClickBook

ClickBook es una plataforma que recomienda libros personalizados usando inteligencia artificial.

## Tecnologías Utilizadas

- **Backend:** Django (Python)
- **IA:** OpenAI (API)
- **Frontend:** Bootstrap, HTML, CSS, JavaScript
- **Base de datos:** SQLite
- **Dependencias adicionales:** numpy, python-dotenv, pandas, Pillow

## Instalación y Configuración

1. Clona este repositorio:
   ```bash
   git clone https://github.com/arendonc2/ClickBook.git
   ```

2. Accede al directorio del proyecto:
   ```bash
   cd ClickBook
   ```

3. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

4. Activa el entorno virtual:
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```

5. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

6. **Adjunta el archivo `.env` que se te proporcionará por aparte** en la raíz del proyecto. Este archivo contiene tu clave de API de OpenAI, por ejemplo:
   ```env
   OPENAI_API_KEY=tu_clave_aquí
   ```

7. Aplica las migraciones de base de datos:
   ```bash
   python manage.py migrate
   ```

8. (Opcional) Crea un superusuario para acceder al panel de administración:
   ```bash
   python manage.py createsuperuser
   ```

9. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

10. Accede a la aplicación en tu navegador:
   ```
   http://127.0.0.1:8000/
   ```

