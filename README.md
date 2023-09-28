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


## WHAT'S IN THE APP

The app contains the following end points: 
![endpoints.png](Extras%2Fimages%2Fendpoints.png)

# HOW TO SETUP THE PROJECT

## THE DOCKER WAY

The easiest way to run the project is to use docker-compose. 
To do so, you need to have docker and docker-compose installed on your machine.

### SETUP DOCKER
### STEP 1 : SETUP ENVIRONMENT

1. Clone the project main branch.
2. Create a `.env.docker` file in the `/app/secrets` directory of the project and add the variables looking at the `.env.example` file.
3. Ensure to set `POSTGRES_HOST=postgres`.
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
3. Visit http://localhost/docs to view the (FastAPI auto generated) API swagger documentation

### DOCKER STRUCTURE

The docker-compose.yml file contains the following services:

1. app: This is the main service that runs the FastAPI application
2. postgres: This is the database service
3. Nginx: This is the web server service

Nginx acts as a reverse proxy to the FastAPI application. 
This is done to allow the application to be served on port 80, also to create a JS based graphql endpoint on the same port.(coming soon...)


## THE NON-DOCKER LOCAL SETUP WAY

--- Coming soon ---
(Hint 1: You can use the docker-compose.yml file as a guide and omit the nginx service)
(Hint 2: Look at Makefile for commands to run the project)

## WHAT NEXT ?

- Admin endpoints
- Head, Options, Patch and Trace endpoints
- GraphQL endpoint (JS based)
