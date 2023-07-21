<h1 align="center">Social networking application</h1>

![статус](https://github.com/exp-ext/social_network/actions/workflows/main.yml/badge.svg?event=push)

<table border="0" cellpadding="0" cellspacing="0" align="center">
    <tr>          
        <td rowspan="2">
            <img src="https://github.com/exp-ext/social_network/blob/main/backend/src/static/img/main.jpeg" width="400">
        </td>
        <td>
            <img src="https://github.com/exp-ext/social_network/blob/main/backend/src/static/img/up.jpeg" width="200">
        </td>
    </tr>
     <tr>
        <td>
            <img src="https://github.com/exp-ext/social_network/blob/main/backend/src/static/img/down.jpeg" width="200">
        </td>
    </tr>
</table>

<hr />

# Test Task for Webtronics FastAPI candidate


## Description

Create a simple RESTful API using FastAPI for a social networking application


## Functional requirements:

- There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
- As a user I need to be able to signup and login
- As a user I need to be able to create, edit, delete and view posts
- As a user I can like or dislike other users’ posts but not my own 
- The API needs a UI Documentation (Swagger/ReDoc)


## Requirements

```
fastapi==0.100.0
fastapi-users==12.0.0
fastapi-cache2==0.2.1
SQLAlchemy==2.0.18
alembic==1.11.1

celery==5.3.1
redis==4.6.0

pytest==7.4.0
pytest-asyncio==0.21.0
```


## Project Organization

- The project runs in Docker containers whose image is pushed in DockerHub.

### To run the project:

- Clone the repository to the local computer;
- Create the /infra/.env file. The template to populate the file is in /infra/.env.example;
- In the infra folder, run the `docker compose up -d --build` command;


## API Documentation

```
http://localhost:8000/docs
```


<hr />

<h3>Project author:</h3>

<p>Borokin Andrey</p>


GITHUB: [exp-ext](https://github.com/exp-ext)

[![Join Telegram](https://img.shields.io/badge/My%20Telegram-Join-blue)](https://t.me/Borokin)