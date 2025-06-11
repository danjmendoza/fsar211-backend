FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Install dependencies
COPY requirements*.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY ./app /app

# Set up alembic.ini from sample
COPY ./app/alembic.ini.sample /app/alembic.ini

# Set working directory
WORKDIR /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]