# tidify-server
> Team Testo bookmark server(tidify)

[![Deploy](https://github.com/Nexters/tidify-server/actions/workflows/main.yml/badge.svg)](https://github.com/Nexters/tidify-server/actions/workflows/main.yml)

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

## ci/cd
> github action + heroku


## heroku ping
> heroku free는 30분동안 트래픽이 없으면 idle로 들어간다. 이를 방지 하기 위한 cron job (16h max per day)

- 최종적으로 960분 깨어있을 수 있기 때문에, 1440/960(1.5) * 30 = 45 min 간격으로 쏜다면 나머지 8시간(45-30 * 32)을 확보 가능
- [Kaffeine](https://kaffeine.herokuapp.com/)은 30분 간격으로 고정 되어있기 때문에, [cronjob](https://cron-job.org/) 사용


## refs
- [Heroku tips](https://towardsdatascience.com/how-to-deploy-your-fastapi-app-on-heroku-for-free-8d4271a4ab9)
- [github action with heroku](https://jarmos.netlify.app/posts/using-github-actions-to-deploy-a-fastapi-project-to-heroku/)
- [heroku container with action tips](https://github.com/AkhileshNS/heroku-deploy/issues/45)
- [simple-crud-async](https://github.com/testdrivenio/fastapi-crud-async)
- [fullstack-fastapi-repo](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)
- [heroku-docker-compose](https://devcenter.heroku.com/articles/local-development-with-docker-compose)