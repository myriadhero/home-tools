# Home tools with Django

This Django project contains Jar app - used to store activities/things/movies/etc and help pick an item of the moment. It's originally for when browsing netflix takes more than a few minutes... Access via /jar/.

In the future I'll be adding other life convenience tools to this project.


## Prerequisites

- Python 3.9 (for compatibility with Rpi)
- Pipenv
  - `pip install pipenv`
- In the root folder create `.env` file
  - Add `DJANGO_DEBUG=true` to it to be able to run the server locally in debug mode
- Navigate to root folder and run
  - `pipenv install`
  - `pipenv run migrate`
  - `pipenv run createsuperuser`
  - `pipenv run django`
- Go to /admin and add the first Jar Category
- Go to /jar

## WIP - Docker

Currently learning docker deployment. 

⚠ This is not a secure or recommended implementation.

https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

Install docker - https://www.docker.com/products/docker-desktop/

In the `.env` file in the root folder, add:

```
DOCKER_CODE_DIR="/user/src/django_server"
DOCKER_WORLD_PORT=8000
```

Create `.env.django_prod` file in the root folder with the following:

```
DJANGO_ALLOWED_HOSTS="localhost,yoursite.com"
DJANGO_DEBUG=false
SECRET_KEY="add you own secret key, 50+ characters long"
```

Modify the variables how you need.

Run:
- `docker compose build`
- `docker compose up -d`
  - Currently, Django uses SQLite from the `/backend` directory, you'll likely need to create first by running pipenv commands in the prereqs above
- `docker compose exec web python app/manage.py collectstatic`

Navigate to http://localhost:8000/jar

If all is successful and you have a category created from the prereqs section, you should be able to see the jar app with bootstrap theme and fontawesome icons - the icons will be missing if collectstatic step isn't done.

🥳🎉