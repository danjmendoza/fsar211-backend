FROM --platform=linux/amd64 tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code
COPY ./app /app

# Set up alembic.ini
COPY ./app/alembic.ini /app/alembic.ini

# Set working directory
WORKDIR /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]