# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files and the serialized model
COPY app.py .
COPY superkart_model.joblib .

# Expose port 7860 for incoming API traffic
EXPOSE 7860

# Run Flask application
CMD ["python", "app.py"]
