# Use the base Python image
FROM python:3.10
RUN set -xe

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
ENV PATH="/root/.local/bin:$PATH"
RUN poetry --version

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry install

# Creating folders, and files for a project:
COPY /app/ /app/app
COPY main.py /app

# Intiate the python server and expose port 8000
CMD ["poetry","run","python", "main.py"]
EXPOSE 8000
