# Matchd Backend

## Introduction

Matchd is a job matching system that matches candidates to companies based on a number of factors, making the screening process much easier for recruiters and thus facilitating the talent search process for companies.

[![.github/workflows/branch_main.yml](https://github.com/matchd-ch/matchd-backend/actions/workflows/branch_main.yml/badge.svg)](https://github.com/matchd-ch/matchd-backend/actions/workflows/branch_main.yml)

## Getting started

Matchd is a Python, Django based project with a Wagtail CMS and uses a GraphQL as its main (and only) API. A local development environment is available to quickly get up and running.

- Install [asdf](https://github.com/asdf-vm/asdf)
- Install [asdf-python](https://github.com/danhper/asdf-python)
- Make sure to have
  - Linux:
    - `apt-get install libmysqlclient-dev`
    - `apt-get install libsqlite3-dev`
  - Mac:
    - `brew install mysql-client`
    - `brew install sqlite3`
    - `brew install libmagic`
- `pip install pipenv`
- `pipenv install`
- If `pipenv install` not work, run `asdf reshim`. After that run `pipenv install` again.
- Start your docker application (Docker Desktop)

```console
# ---------------------------
# Run mariadb
# ---------------------------

$ docker volume create mariadb
$ docker run \
  --restart always \
  --name mariadb \
  -v mariadb:/var/lib/mysql \
  -p 3306:3306 \
  -d \
  -e MYSQL_ROOT_PASSWORD="" \
  -e MYSQL_ALLOW_EMPTY_PASSWORD=1 \
  mariadb:latest
```

```console
# ---------------------------
# Run elasticsearch
# ---------------------------

$ docker run \
    --restart always \
    -d \
    -p 9200:9200 \
    -e discovery.type=single-node \
    -e xpack.security.enabled=false \
    --name elasticsearch \
    elasticsearch:8.5.1
```

```console
# ---------------------------
# Run maildev
# ---------------------------

$ docker run \
    --restart always \
    -d \
    -p 25:25 \
    -p 9123:8080 \
    --name maildev \
    djfarrelly/maildev \
    maildev \
    --smtp 25 \
    --web 8080
```

- Copy `.env.dist` to `.env` and correct necessary settings
- `pipenv run setup`
- `pipenv run start`

## Admin GUI

You can access the Admin gui through <a href="http://api.matchd.localhost:8000/admin/"> http://api.matchd.localhost/admin </a>. Username is `admin` and password is `admin`.

## Django Admin GUI

You can access the Admin gui through <a href="http://api.matchd.localhost:8000/django-admin/"> http://api.matchd.localhost/django-admin/ </a>. Username is `admin` and password is `admin`.

## GraphQL-API

The GraphQL Endpoint is available under [http://api.matchd.localhost:8000/graphql](http://api.matchd.localhost:8000/graphql)

In order not to run into csrf token issues, you need to make a GET request to http://api.matchd.localhost:8000/csrf. This request will properly set the csrf cookie.

For all future requests to the graphql endpoint, you need to include the cookie in the request. In addition you need to set a custom header:

```
X-CSRFToken: <YOUR CSRF TOKEN HERE>
```

If you want to access user specific data you also need to include the authorization header:

```
Authorization: JWT <YOUR JWT TOKEN HERE>
```

## MailDev Email Admin

You can access the email admin page at `localhost:9123` (or a different port if you choose another port when running [the MailDev docker run command](https://github.com/matchd-ch/matchd-backend#getting-started)). This can be useful for verifying the emails that are being sent by the backend and for email/newsletter development.

## Project details

The project requires a bunch of environment variables at startup. Those variables and their description can be found in `.env.dist`. The project looks automatically for a file named `.env` in the root directory to retrieve the required variables at startup.

### Database Models

The primary database models: _Users_, _Employees_, _Students_ and _Companies_. The _User_ is the entry point to interact with the system. A user can be a _Student_, _Employee_ (internal, for example a "recruiter") or be related to a _Company_.

### Matching process

The matching process is a recommending system that is used for suggesting _Job Posting_(s) to students.
The following environment variables (found in `app/settings/base.py`) are used when calculating a matching score between a job posting and a student:

```
MATCHING_VALUE_BRANCH = 0
MATCHING_VALUE_JOB_TYPE = 3
MATCHING_VALUE_WORKLOAD = 1
MATCHING_VALUE_CULTURAL_FITS = 3
MATCHING_VALUE_SOFT_SKILLS = 3
MATCHING_VALUE_KEYWORDS = 3
MATCHING_VALUE_SKILLS = 3
MATCHING_VALUE_LANGUAGES = 2
MATCHING_VALUE_DATE_OR_DATE_RANGE = 5
```

The variables are used as _boosts_ in the searching process; each variable increases the relevance / importance of the related topic.
The highest score value is calculated based on a subset of those variables, such score is used to normalize the retrieved search results, also called _hits_.

The system uses _elasticsearch_ to perform the search (via the Wagtail search backend) and uses the _score_ values provided in the results to calculate the final score list. A _match mapper_ is then used to match each element of the score list to a desired list of targets (e.g. match map Student to Job Posting).

## Test Data

_! Do not use dump_data / load_data command from django !_

Run following command to seed test data:

```console
docker-compose exec api bash
./manage.py seed
```

Loads all user data from `db/seed/data/fixtures.json`

See `ACCOUNTS.md` for all available user accounts

## Dump Fixtures

```
docker-compose exec api bash
./manage.py dump_seed
```

Creates a dump of all user data including attachments (`db/seed/data/fixtures.json`)

Updates the file `ACCOUNTS.md` with all users

## Create test data

```
docker-compose exec api bash
# 50 students, 100 companies, 200 universities
./manage.py random_seed 50 100 200
```

All users generated with this command will be ignored if you dump fixtures with `dump_seed`

## Zip / City

Download xls file from here: https://postleitzahlenschweiz.ch/tabelle/

Copy the file to api/data/data.xlsx and run the following command:

```
pip install pandas
cd api/data
python xlsx_to_json.py
```

## Email Test Setup

Add the following lines to the `urls.py` for adding testing view.

[app/urls.py](app/urls.py)

```py
from db.view.email_template_test_helper_view import email_template_test_helper_view

urlpatterns = [
    ...
    path('test-email-template/', email_template_test_helper_view),
]
```

## Development workflow

The project conforms to the [pep8](https://www.python.org/dev/peps/pep-0008/) styling guide. We recommend running the following command sequence regularly during your coding sessions, and, mandatorily before creating a pull request (so you don't run into problems with the CI / CD pipeline)

### yapf code formatter

```console
pipenv run format
```

### pylint

```console
pipenv run lint
```

### Tests

```console
pipenv run test
```

With coverage:

```console
pipenv run test --cov=db --cov=api --cov=app --cov-report html
```

## Contributing

You can contribute to the project by opening a pull request that will be peer reviewed. Always run the development workflow commands locally before creating a pull request so that your code conforms to the project's requirements.

## Bugs / Feature Requests

https://github.com/matchd-ch/stories
