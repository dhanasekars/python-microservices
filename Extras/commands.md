
## Postgres
```shell
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres

``` 
Go inside your container and create a database:

```shell
docker exec -it 05b3a3471f6f bash
root@05b3a3471f6f:/# psql -U postgres
postgres-# CREATE DATABASE mytest;
postgres-# \q
```
```shell
psql -h localhost -p 5432 -U postgres

```

```shell
> \l  # inside postgres prompt
# lists all database 
```

Stop tracking after check in

```shell
o```
To start tracking again

```shell
git update-index --no-assume-unchanged FILE_NAME
```