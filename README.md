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
- Modern server-rendered frontend foundation with Django templates, Tailwind, HTMX, and Alpine
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


## Neo4j with Docker (Dev & Prod)

This project uses Docker to run Neo4j for both development and production. All configuration is managed via environment variables.

### Quick Start (Development)

1. Copy `.env.example` to `.env` and edit as needed:
    ```bash
    cp .env.example .env
    # Edit NEO4J_PASSWORD, ports, etc. for your environment
    ```
2. Start Neo4j with Docker Compose:
    ```bash
    docker-compose up -d
    ```
3. Access Neo4j Browser at [http://localhost:7474](http://localhost:7474) (default password: see `.env`)

### Production Notes
- Use strong, unique passwords for `NEO4J_PASSWORD` in production.
- Consider using Docker secrets or your CI/CD system to inject secrets securely.
- Data is persisted in Docker volumes (`neo4j_data`, etc.).
- Adjust memory and other configs in `docker-compose.yml` as needed.

### Stopping Neo4j
```bash
docker-compose down
```

---

## Hybrid Django/Neomodel/Cypher Usage


This project supports both Neomodel ORM and direct Cypher queries via a utility module (`core/neo4j_cypher_utils.py`).

### Usage Patterns

**Neomodel ORM (Recommended for most use cases):**
```python
from movies.neomodels import Film
film = Film.nodes.get(title="Inception")
print(film.release_year)
```

**Direct Cypher Queries (Advanced/Custom):**
```python
from core.neo4j_cypher_utils import run_read_cypher
query = "MATCH (f:Film) WHERE f.release_year >= $min_year RETURN f.title, f.release_year"
results, _ = run_read_cypher(query, {'min_year': 2000})
for title, year in results:
    print(title, year)
```

See `movies/neomodels.py` and `lists/neomodels.py` for more examples. Tests in `movies/tests.py` and `lists/tests.py` also demonstrate usage.

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
- **ReDoc:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **Raw schema:** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)
- Swagger UI includes a custom live search bar for filtering endpoints by path, method, operation ID, and summary text.
- JWT auth is preconfigured for the schema. Use `Bearer <your_access_token>` in the Swagger **Authorize** dialog.

## Frontend Stack

- Django templates for shared server-rendered pages
- Tailwind CSS via CDN for modern layout and utility styling
- HTMX for HTML-over-the-wire interactions
- Alpine.js for lightweight client-side behavior

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
