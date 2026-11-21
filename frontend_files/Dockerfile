# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy frontend requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend application script
COPY app_frontend.py .

# Expose port 8501 for incoming web traffic
EXPOSE 8501

# Run Streamlit application
CMD ["streamlit", "run", "app_frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
