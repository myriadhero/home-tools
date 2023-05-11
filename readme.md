# Home tools with Django

This Django project contains Jar app - used to store activities/things/movies/etc and help pick an item of the moment. It's originally for when browsing netflix takes more than a few minutes... Access via /jar/.

In the future I'll be adding other life convenience tools to this project.


## Prerequisites

- Python 3.9 (for compatibility with Rpi)
- Pipenv
  - `pip install pipenv`
- Navigate to root folder and run
  - `pipenv install`
  - `pipenv run migrate`
  - `pipenv run createsuperuser`
  - `pipenv run django`
- Go to /admin and add the first Jar Category
- Go to /jar

## WIP

Currently learning docker deployment.