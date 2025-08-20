# Use official lightweight Python image
FROM python:3.10-slim

# Set work directory inside container
WORKDIR /app

# Copy requirements file (no "frontend/" prefix)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the frontend code
COPY . .

# Run Streamlit on container startup
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
