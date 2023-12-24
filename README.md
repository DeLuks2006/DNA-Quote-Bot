# DNA-Quote-Bot

A discord bot that spits out a new quote each day.

## Installation

Installation for development with docker

1. Copy .env.example and rename to .env

```bash
cp .env.example .env
```

2. Configure the .env file and start the docker container

```bash
docker compose up
```

3. Database migrations via alembic

```bash
# Connect to the docker container
docker exec -it dna-quote-bot /bin/bash

# Run migrations
alembic upgrade head
```

That's it. The application is running in docker. You can now connect to the docker container and develop.

## Alembic cheatsheet

```bash
# Auto-generate migrations
alembic revision --autogenerate -m "<Migration Name>"

# Run migrations
alembic upgrade head

# Downgrade to previous commit
alembic downgrade -1

# Upgrade to next commit
alembic upgrade +1
```
