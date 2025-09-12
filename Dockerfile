# Use official Python slim image
FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

# Start app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
