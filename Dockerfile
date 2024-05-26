# Use the official Python image as a base
FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y python3-dev gcc libffi-dev

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the command to run the application
CMD ["python", "run.py"]
