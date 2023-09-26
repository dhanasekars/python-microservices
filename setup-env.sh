#!/bin/bash
set -e



# make this script executable
# chmod +x setup-env.sh

# Generate the SQL script to create the database and user
psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres <<EOSQL
  CREATE USER ${TODOLIST_ADMIN} WITH PASSWORD '${TODO_ADMIN_PASSWORD}';
  ALTER USER ${TODOLIST_ADMIN} CREATEDB;
EOSQL


#  CREATE DATABASE ${TODOLIST_DB};
#  GRANT ALL PRIVILEGES ON DATABASE ${TODOLIST_DB} TO ${TODOLIST_ADMIN};
