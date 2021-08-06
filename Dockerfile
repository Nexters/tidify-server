# ------------------------------------------------------------------------------
# Base image
# ------------------------------------------------------------------------------
FROM python:3.8-slim AS base

# ------------------------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------------------------
FROM base AS deps
COPY requirements.txt ./

# ERROR: No matching distribution found for psycopg2==2.9.1
RUN apt update > /dev/null && \
        apt install -y build-essential && \
        pip install --disable-pip-version-check -r requirements.txt

# ------------------------------------------------------------------------------
# Final image
# ------------------------------------------------------------------------------
FROM base
WORKDIR /usr/src/app

COPY ./src /usr/src/app
COPY requirements.txt /usr/src/app/

COPY --from=deps /root/.cache /root/.cache
RUN pip install --disable-pip-version-check -r requirements.txt && \
        rm -rf /root/.cache

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD alembic upgrade head && uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port $PORT

