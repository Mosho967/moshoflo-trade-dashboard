# Use official Python base image
FROM python:3.13.5-slim

# Set working directory
WORKDIR /app

# Copy dependencies file first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
