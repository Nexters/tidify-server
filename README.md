# tidify-server
> Team Testo bookmark server(tidify)

## dep
```
pip install fastapi 'uvicorn[standard]' SQLAlchemy alembic PyJWT psycopg2
```

## dev
```bash
# /tidify-server/src
$ docker compose -f docker-compose.dev.yml up
$ alembic revision --autogenerate -m "<write_here_migration_name>" 
$ alembic upgrade head
$ python main.py
$ docker compose -f docker-compose.dev.yml down --rmi local 
```

## sandbox setup

```
$ heroku git:remote -a tidify
$ heroku container:login
$ heroku container:push web
$ heroku container:release web
$ heroku open
```







## refs
- [simple-crud-async](https://github.com/testdrivenio/fastapi-crud-async)
- [fullstack-fastapi-repo](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)
- [heroku-docker-compose](https://devcenter.heroku.com/articles/local-development-with-docker-compose)