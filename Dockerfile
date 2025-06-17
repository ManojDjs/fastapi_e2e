FROM python:3.12-slim

WORKDIR /code

# Copy the project files for depenedency and env management

COPY pyproject.toml poetry.lock /code/
# Install poetry and project depenedencies with poetry
RUN pip install poetry

RUN poetry install --no-root

# Copy app folder into the working directory with app folder similar to our project structure
COPY /src /code/src

# expose port to access the api
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main:app" ,"--host", "0.0.0.0", "--port", "8000","--workers","4" ]