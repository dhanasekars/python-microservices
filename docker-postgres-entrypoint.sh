#!/bin/bash
set -e

# Generate a SQL script with dynamic user creation
echo "CREATE USER ${TODOLIST_ADMIN} WITH PASSWORD '${TODO_ADMIN_PASSWORD}';" > /docker-entrypoint-initdb.d/init.sql

/docker-entrypoint.sh "$@"
