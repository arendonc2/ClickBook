# ClickBook

## Tecnologías Utilizadas
- **Backend:** Django (Python)
- **Frontend:** Bootstrap, HTML, CSS, JavaScript
- **Base de datos:** SQLite

## Instalación y Configuración

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/ClickBook.git
   ```
2. Accede al directorio del proyecto:
   ```bash
   cd ClickBook
   ```
3. Crea un entorno virtual e instálalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```
6. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
7. Accede a la aplicación en tu navegador en `http://127.0.0.1:8000/`.

