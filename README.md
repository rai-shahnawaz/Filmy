db.sqlite3
docker-compose.yml
git clone <repository-url>
cd Filmy
docker-compose up --build
docker-compose down

# Filmy

Filmy is a modular Django web application for managing movies, series, celebrities, user profiles, reviews, recommendations, and more. It provides a RESTful API, JWT authentication, and interactive API documentation using Swagger (drf-spectacular).

---

## Features
- Movie, series, and celebrity management
- User authentication and profiles
- User-created lists and favorites
- Reviews and ratings
- Recommendations engine
- JWT-based authentication
- RESTful API endpoints for all modules
- Interactive API docs (Swagger & Redoc)
- Static and media file handling

---

## Project Structure

```
db.sqlite3
manage.py
Procfile
requirements.txt
core/
    asgi.py
    settings.py
    urls.py
    wsgi.py
auth/
    ...
lists/
    ...
movies/
    ...
people/
    ...
recommendations/
    ...
reviews/
    ...
users/
    ...
static/
    css/
    fonts/
    images/
    js/
templates/
    *.html
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd Filmy
    ```
2. **(Optional) Create a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Apply migrations**
    ```bash
    python manage.py migrate
    ```
5. **Run the development server**
    ```bash
    python manage.py runserver
    ```
6. **Access the application**
    - Open your browser at: http://127.0.0.1:8000/

---

## API Documentation

- **OpenAPI/Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Redoc:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **Raw schema:** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

### Authentication
- Obtain a JWT token via the `/api/auth/` endpoints.
- Authorize in Swagger UI with: `Bearer <your_access_token>`

---

## Running Tests

To run all tests:
```bash
python manage.py test
```

---

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

---

## License
Specify your license here (e.g., MIT, GPL, etc.)

---

## Contact
Add your contact information or project links here.
