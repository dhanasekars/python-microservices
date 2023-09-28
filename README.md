# A web API project primarily for software testing purposes

## Technology stack
- Python 3.8
  - FastAPI
  - Pytest
  - SQLAlchemy
  - Poetry
  - Pydantic
- PostgreSQL
- Docker
  - Docker Compose
- Nginx


# HOW TO SETUP THE PROJECT

## DOCKER WAY

The easiest way to run the project is to use docker-compose. 
To do so, you need to have docker and docker-compose installed on your machine.

### SETUP 1 : SETUP ENVIRONMENT

1. Clone the project main branch
2. Create a .env.docker file in the app/secrets directory of the project and add the variables looking at the `.env.example` file.
3. Ensure to set `POSTGRES_HOST=postgres`
4. Run the following to make execute permissions on the setup-env.sh file:
    ```bash
    chmod +x setup-env.sh
    ```

### STEP 2 : BUILD AND RUN THE PROJECT

1. Run the following command to build the project:
    ```bash
	    docker-compose build
    ``` 
2. Run the following command to run the project:
    ```bash
    docker-compose --env-file app/secrets/.env.docker up
    ```
3. Visit http://localhost/docs to view the API documentation

### DOCKER STRUCTURE

The docker-compose.yml file contains the following services:

1. app: This is the main service that runs the FastAPI application
2. postgres: This is the database service
3. nginx: This is the web server service

Note: nginx acts as a reverse proxy to the FastAPI application. 
This is done to allow the application to be served on port 80, also to create a graphql endpoint on the same port.(coming soon...)



