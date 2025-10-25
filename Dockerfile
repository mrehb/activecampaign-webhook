FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "webhook:app"]