# Filmy

Filmy is a web application project designed to manage and display movie, series, and celebrity information. It is built using Django and follows a modular structure for scalability and maintainability.

## Project Structure

```
db.sqlite3
Dockerfile
docker-compose.yml
manage.py
requirements.txt
core/
    asgi.py
    settings.py
    urls.py
    wsgi.py
media/
    images/
        blank.html
snippets/
    admin.py
    apps.py
    decorators.py
    models.py
    serializers.py
    tests.py
    urls.py
    views.py
static/
    css/
    fonts/
    images/
    js/
templates/
    *.html
```

## Features
- Movie, series, and celebrity management
- User profiles and favorites
- RESTful API endpoints (see `snippets/`)
- Static and media file handling
- Docker support for easy deployment

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (optional, for containerized deployment)
- pip (Python package manager)

### Installation

#### 1. Clone the repository
```bash
git clone <repository-url>
cd Filmy
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Apply migrations
```bash
python manage.py migrate
```

#### 4. Run the development server
```bash
python manage.py runserver
```

#### 5. Access the application
Open your browser and go to `http://127.0.0.1:8000/`

### Using Docker

#### Build and run with Docker Compose
```bash
docker-compose up --build
```

#### Stopping the containers
```bash
docker-compose down
```

## Project Modules

- **core/**: Django project settings and configuration
- **snippets/**: Main app for movies, series, celebrities, and user features
- **media/**: Uploaded media files
- **static/**: Static assets (CSS, JS, images)
- **templates/**: HTML templates for frontend

## API Endpoints
API endpoints are defined in `snippets/urls.py` and handled by `snippets/views.py`. For details, see the code or use the Swagger UI at `/swagger_ui.html` (if enabled).

## Running Tests
    - **media/**: Uploaded media files
python manage.py test snippets
```

## Contributing
    API endpoints are defined in `urls.py` and handled by `views.py`. For details, see the code or use the Swagger UI at `/swagger_ui.html` (if enabled).
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## License
Specify your license here (e.g., MIT, GPL, etc.)

## Contact
Add your contact information or project links here.
