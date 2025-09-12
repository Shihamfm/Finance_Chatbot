# Use official Python slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port for Cloud Run (optional, helps readability)
EXPOSE 8080

# Start the app (Cloud Run provides PORT environment variable)
CMD ["python", "app.py"]
