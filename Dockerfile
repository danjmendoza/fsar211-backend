FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./app /app
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]