# Module Web App

## Objective:
* An application with a minimal frontend, backend and db to register kids id and their image to authentify.
* Will be used by kids and their teacher to monitor the robot and the data.
* A form could be use to register a new kid with its image.
* Teacher could have permission to modify the db from a form.
* Serveur local + Base de donnée sur le raspberry pi.
* ou bien: Client - Serveur

## Exemple tech stack: 
* Python flask, sqlite db (python sqlite standard lib), simple html/css/js form+buttons
    * exemple here : python3 app.py
* Php...
* Nodejs...

## Frontend

- Basic authentication with hardcoded password at `/admin`
- Visitors can only access the login page. Other pages redirect to `/admin/login`.
- Authentication persists across the session: user can reload/change the page and stay connected.
- A logged-in user can logout.


The following routes are available for authenticated users: 
- `/admin/add` A form to add a new user
- `/admin/list` List users, there's a delete button next to each user. An optional "name" GET parameter filters user by name example `/admin/list?name=toto`
- `/admin/search` a basic form with one input and a search button, this redirects to `/admin/list?name=<input_content>`
- `/admin/logout` Logout the user and redirect to the login page

## API

A REST API is available. The documentation is available at `/api/doc`. It is powered by (swagger-ui)[https://swagger.io/tools/swagger-ui/].
TODO: The API is not protected by authentication and is available to visitor.

## Feature

- The app generate and store thumbnail for user image

## Models

### User

- `created_at`: creation timestamp
- `picture`: info about the user uploaded picture, contains path, thumbnail_path and media related information. The picture file itself is stored on the filesystem at `static/images` and `static/thumbnail`
- `openai_chat_messages` The JSON (as string) openai chat conversation history.
- `first_name`
- `last_name`

## Database manipulation

You can either request the API or use directly the Data-Access-Object helper (used by the API).

```py
#! venv/bin/python3

import threading
import time
import requests

from module_webapp import create_app
from module_webapp.dao.user import user
from flask import url_for


def dao_print_users():
    with app.app_context():
        print("DAO print users:")
        for u in user.getAll():
            print(u.name)


def api_print_users():
    print("API print users:")

    response = requests.get("http://localhost:5000/api/users")
    if response.status_code == 200:
        data = response.json()
        for u in data:
            print(u["name"])
    else:
        print("Request failed:", response.status_code)


def print_user_twice():
    time.sleep(2)
    dao_print_users()
    time.sleep(2)
    api_print_users()


if __name__ == "__main__":
    app = create_app()
    threading.Thread(target=print_user_twice).start()
    app.run(debug=True)
```

## Dependencies
- [sqlalchemy 2](https://www.sqlalchemy.org/) SQL toolkit and ORM
- [sqlalchemy_media](http://sqlalchemy-media.dobisel.com/) For image validation, processing, storage and db thumbnail generation
- [flask](https://flask.palletsprojects.com/) Micro web framework
- [flask-restx](https://flask-restx.readthedocs.io/en/latest/) For swagger API documentation generation
- [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) An extension for Flask that adds support for SQLAlchemy

In `requirements.txt`:

```
Flask==2.3.2
flask-restx==1.1.0
sqlalchemy-media==0.17.4
SQLAlchemy==2.0.20
Flask-SQLAlchemy==3.0.5
```
