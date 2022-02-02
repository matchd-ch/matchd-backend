# Matchd Backend

[![.github/workflows/branch_main.yml](https://github.com/matchd-ch/matchd-backend/actions/workflows/branch_main.yml/badge.svg)](https://github.com/matchd-ch/matchd-backend/actions/workflows/branch_main.yml)

## Development Setup

* Install [asdf](https://github.com/asdf-vm/asdf)
* Install [asdf-python](https://github.com/danhper/asdf-python)
* `pip install pipenv`
* `pipenv install`
* Make sure to have `apt-get install libmysqlclient-dev` and `apt-get install libsqlite3-dev`
* Run `mariadb`  
```console
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
* Run `elasticsearch`  
```console
docker run \
    --restart always \
    -d \
    -p 9200:9200 \
    -e discovery.type=single-node \
    --name elasticsearch \
    elasticsearch:7.16.1
```
* Run `maildev`  
```console
docker run \
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
* Copy `.env.dist` to `.env` and correct necessary settings
* `pipenv run setup`
* `pipenv run start`

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

## Test Data

*! Do not use dump_data / load_data command from django !*

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

## Testing

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
    
