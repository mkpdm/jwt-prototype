# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY Pipfile.lock .

# Install the dependencies
RUN pip install pipenv && pipenv sync

# Copy the FastAPI app code into the container
COPY ./mkapi .

# Command to run the FastAPI app with Uvicorn
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]