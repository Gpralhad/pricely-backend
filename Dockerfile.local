# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# (Make sure to include fastapi, uvicorn, and sqlalchemy in requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder into the container
COPY . .

# Set the PYTHONPATH so the app can find the 'common' module
ENV PYTHONPATH=/app

# Command to run the discovery service
CMD ["uvicorn", "discovery_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
