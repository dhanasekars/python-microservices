# A CRUD Web microservices app using FastAPI

- The project can be used as an example to learn how to build a web API using FastAPI and PostgreSQL.
- To learn how to write unit and integration tests for a web API.
- This project has 100% unit and 90% integration test coverage. (does that mean it is bug-free?)
- What is covered in automated checks and exploratory tests to find bugs.

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
- JS
  - nodejs
  - Babel
  - graphql-yoga
  - babel-plugin-transform-object-rest-spread
  - graphql-subscriptions


## WHAT'S IN THE APP

The app contains the following endpoints: 

![endpoints.png](Extras%2Fimages%2Fendpoints.png)

# HOW TO SET UP THE PROJECT

## THE DOCKER WAY

The easiest way to run the project is to use docker-compose. 
To do so, you will need to have docker and docker-compose installed on your machine.

### SETUP DOCKER
### STEP 1: SETUP ENVIRONMENT

1. Clone the project's main branch.
2. Create a `.env.docker` file in the `/app/secrets` directory of the project and add the variables looking at the `.env.example` file.
3. Ensure to set `POSTGRES_HOST=postgres`.
4. Run the following to execute permissions on the setup-env.sh file:
    ```bash
        chmod +x setup-env.sh
    ```

### STEP 2: BUILD AND RUN THE PROJECT

1. Run the following command to build the project:
    ```bash
	    docker-compose build
    ``` 
2. Run the following command to run the project:
    ```bash
       docker-compose --env-file app/secrets/.env.docker up
    ```
3. Visit http://localhost/docs to view the (FastAPI auto-generated) OpenAPI documentation

### DOCKER STRUCTURE

The docker-compose.yml file contains the following services:

1. app: This is the main service that runs the FastAPI application
2. postgres: This is the database service
3. Nginx: This is the web server service

Nginx acts as a reverse proxy to the FastAPI application. 
This allows the application to be served on port 80 and create a JS-based graphql endpoint on the same port. (coming soon...)

## THE NON-DOCKER LOCAL SETUP WAY

Unlike Docker, local setup requires more work to get the project running.


### STEP 1: SETUP APP
1. Clone the project's main branch.
2. Install Poetry on your machine. Project dependencies are managed using Poetry.( https://python-poetry.org/docs/#installation )
3. Run the following command to install the project dependencies:
    ```bash
        poetry install
    ```
4. Create a `.env.local` file in the `/app/secrets` directory of the project and add the variables looking at the `.env.example` file. Ensure to set `POSTGRES_HOST=localhost`.
5. Set `MY_ENVIRONMENT=local`
        ```bash
        export MY_ENVIRONMENT=local ```

### STEP 2: SETUP DATABASE

1. The CRUD app needs a PostgreSQL database to run. You can install PostgreSQL on your machine or use docker to run a PostgreSQL container.
2. The app needs a username and password to connect to the database. 
3. The app creates the database on startup. Ensure to set the database name in the `.env.local` file.
4. Create a user with the name specified in the `.env.local` file.
5. The app looks for a username and password in the `.env.local` file. Please set the password for the user you created in step 2.
6. Look at Makefile to see the commands to run to tests and run the project.

### STEP 3: RUN THE PROJECT

1. Run the following command to run the project:
    ```bash
      cd app &&
      poetry run python main.py
    ```

`Unlike the Docker setup, the local setup steps were not tested. You may need to do some debugging to get the project running.`


### A lite version

The project's lightweight no database version is available at [simple-crud](https://github.com/dhanasekars/simple-crud-microservices) repo.
This app uses a JSON to store data.

## WHAT NEXT?

### 2023 Q4
- Admin endpoints to manage users, roles and data
- Head, Options, Patch and Trace endpoints
- JS GraphQL endpoint
- JS GraphQL endpoint tests
