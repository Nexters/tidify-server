# tidify-server
> Team Testo bookmark server(tidify)

## dep
```
pip install fastapi 'uvicorn[standard]' SQLAlchemy alembic PyJWT psycopg2-binary pytest-asyncio
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
```

```
$ docker build -t web .
$ heroku container:login
$ heroku container:push web
$ heroku container:release web
$ heroku open
```

## heroku ping
> heroku free는 30분동안 트래픽이 없으면 idle로 들어간다. 이를 방지 하기 위한 cron job (16h max per day)

- [Kaffeine](https://kaffeine.herokuapp.com/)
- Heroku requires all free applications to sleep for 6 hours every day.

## refs
- [Heroku tips](https://towardsdatascience.com/how-to-deploy-your-fastapi-app-on-heroku-for-free-8d4271a4ab9)





## refs
- [simple-crud-async](https://github.com/testdrivenio/fastapi-crud-async)
- [fullstack-fastapi-repo](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)
- [heroku-docker-compose](https://devcenter.heroku.com/articles/local-development-with-docker-compose)