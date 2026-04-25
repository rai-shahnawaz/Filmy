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



## Neo4j Hybrid Setup: Docker (Dev) & Aura (Prod)

This project uses a hybrid approach for Neo4j:
- **Dockerized Neo4j** for local/dev (on your machine or a VPS)
- **Neo4j Aura** (managed cloud) for production

All configuration is managed via environment variables for easy switching.

### Quick Start: Local/Dev (Docker)

1. Edit `.env` as needed (see comments in file):
    - Set `NEO4J_PASSWORD`, `NEO4J_HTTP_PORT`, `NEO4J_BOLT_PORT`, etc.
2. Start Neo4j with Docker Compose:
    ```bash
    docker-compose up -d
    ```
3. Access Neo4j Browser at [http://localhost:7474](http://localhost:7474) (default password: see `.env`)

#### Running Neo4j on a VPS (Optional)
- You can run the same Docker Compose setup on a VPS (e.g., Oracle Cloud) for remote dev.
- Update `.env` and firewall rules as needed.

### Production: Neo4j Aura

1. Create a Neo4j Aura instance (https://console.neo4j.io/)
2. In your Render (or other host) dashboard, set these environment variables:
    - `NEOMODEL_NEO4J_BOLT_URL=bolt+s://<username>:<password>@<host>:<port>`
    - `NEOMODEL_ENCRYPTED_CONNECTION=True`
3. Do NOT use Docker Compose for Neo4j in production.

### Switching Environments
- Local/dev: Uses Docker Compose and `.env` for config
- Production: Uses Aura connection string and encrypted connection via env vars

### Stopping Neo4j (Dev)
```bash
docker-compose down
```

---


## Hybrid Django/Neomodel/Cypher Usage

This project supports both:
- **Neomodel ORM** for most graph modeling
- **Raw Cypher queries** via a utility module (`core/neo4j_cypher_utils.py`)

See `movies/neomodels.py` and `lists/neomodels.py` for examples. Tests in `movies/tests.py` and `lists/tests.py` demonstrate both patterns.

### How to Use

**Neomodel ORM (Recommended):**
```python
from movies.neomodels import Film
film = Film.nodes.get(title="Inception")
print(film.release_year)
```

**Raw Cypher Utility:**
```python
from core.neo4j_cypher_utils import run_cypher
query = "MATCH (f:Film) WHERE f.release_year >= $min_year RETURN f.title, f.release_year"
results, _ = run_cypher(query, {'min_year': 2000})
for title, year in results:
    print(title, year)
```

---

## Environment Variable Reference

- `.env` (local/dev):
    - `NEO4J_PASSWORD`, `NEO4J_HTTP_PORT`, `NEO4J_BOLT_PORT`, `NEO4J_USER`
- Render/prod:
    - `NEOMODEL_NEO4J_BOLT_URL`, `NEOMODEL_ENCRYPTED_CONNECTION`

---

## Verification Checklist

1. Start Neo4j via Docker (local or VPS), confirm browser and Bolt access
2. Start Django, confirm ORM and Cypher utility work
3. Deploy to Render with Aura config, confirm production works
4. Run all tests
5. Review documentation for clarity

---

## Further Considerations

1. For production, always use a managed Neo4j (Aura or your own server), not Docker Compose on Render
2. For dev, you can use Docker locally or on a VPS
3. Document any future AI/GraphRAG or Rust/Vector features separately

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
