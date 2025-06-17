
# 🚀 FastAPI E2E Project

This is a production-ready FastAPI project using a clean layered architecture:

- **API Layer**: Handles HTTP routes
- **Service Layer**: Business logic
- **Repository Layer**: Database interaction
- **Pydantic Layer**: Validation and ORM schemas
- **SQL DB Layer**: SQLAlchemy models
- **Tested**: Unit tested across all layers

---

## 📁 Project Structure






---

## 🧱 Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** – High-performance async API framework
- **[Pydantic](https://docs.pydantic.dev/)** – Data validation and parsing
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – ORM for relational databases
- **[Poetry](https://python-poetry.org/)** – Python dependency management
- **[Pytest](https://docs.pytest.org/)** – Testing framework

---

## ✅ Features

- ✨ Modular and scalable architecture
- 🔒 Input/output validation via Pydantic
- 🧠 Separation of concerns: API, Service, Repository layers
- 🧪 Unit tested at each layer for reliability
- 📦 Ready for Docker deployment (optional)

---

## ⚙️ Setup

### 1. Clone the repository 🍴

```bash
git clone https://github.com/yourusername/fastapi_e2e.git
cd fastapi_e2e
```
### 2. install dependencies 👨🏻‍💻
```
 poetry install
 poetry run uvicorn src.main:app --reload
 poetry add [any new library]
 poetry update # for letest version of dependencies
```
### 3. Running Tests 🧪
```
poetry run pytest . # for all tests
poetry run pytest [path] #for specefic tests
```
### 4.Documentation
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

### 5. Docker 
```
docker-compose build
docker-compose up
```
docker

# Linting
used ruff for this project

##### To run ruff
    poetry run ruff check .

###### To run ruff for formatting 
                
    poetry run ruff format .

##### to run ruff for sorting like Isort

    poetry run ruff check --select I --fix .

##### Rules for ruff are given in .toml file

You can update are append these rules according to project guide.
once updated .toml file. Please, run these commands

    poetry lock # for locking .toml file
    poetry install
    poetry ruff [check/format] [path/.]