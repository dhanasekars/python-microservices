# Use the base Python image
FROM python:3.89-slim

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies using Poetry
RUN poetry install

# Copy your project files to the container
COPY . /app/

# Define the command to run your Python application
CMD ["python", "your_app.py"]

