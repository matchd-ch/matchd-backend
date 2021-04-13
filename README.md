Matchd Backend
==============

# Admin GUI
You can access the Admin gui through <a href="http://api.matchd.lo/admin/"> http://api.matchd.lo/admin </a>. Username is `admin` and password is `admin`.

# Django Admin GUI
You can access the Admin gui through <a href="http://api.matchd.lo/django-admin/"> http://api.matchd.lo/django-admin/ </a>. Username is `admin` and password is `admin`.

# GraphQL-API
The GraphQL Endpoint is available under [http://api.matchd.lo/graphql](http://api.matchd.lo/graphql)

In order not to run into csrf token issues, you need to make a GET request to http://api.matchd.lo/csrf. This request will properly set the csrf cookie.


For all future requests to the graphql endpoint, you need to include the cookie in the request. In addition you need to set a custom header:

    X-CSRFToken: <YOUR CSRF TOKEN HERE>
    
If you want to access user specific data you also need to include the authorization header:

    Authorization: JWT <YOUR JWT TOKEN HERE>

# Test Data

*! Do not use dump_data / load_data command from django !*

Run following command to seed test data:

    docker-compose exec api bash
    ./manage.py seed

Loads all user data from `db/management/data/fixtures.json`

See `ACCOUNTS.md` for all available user accounts

# Dump Fixtures

    docker-compose exec api bash 
    ./manage.py dump_seed

Creates a dump of all user data including attachments (`db/management/data/fixtures.json`)

Updates the file `ACCOUNTS.md` with all users

# Create test students

    docker-compose exec api bash 
    ./manage.py dummy_students 100

All users generated with this command will be ignored if you dump fixtures with `dump_seed`

# Zip / City

Download xls file from here: https://postleitzahlenschweiz.ch/tabelle/

Copy the file to api/data/data.xlsx and run the following command:

    pip install pandas
    cd api/data
    python xlsx_to_json.py

# Testing

## pylint

    docker-compose exec api bash
    pylint api app db

## Tests

    docker-compose exec api bash
    ./manage.py pytest
