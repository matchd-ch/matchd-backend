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

# Registered / Verified users


| Type | Username | Password |
|---|---|---|
| Company | john@doe.com | asdf1234$ |
| University | joe@doe.com | asdf1234$ |
| Student | jane@doe.com | asdf1234$ |


# Dump Fixtures

## Users

    docker-compose exec api bash
    ./manage.py dumpdata --indent 4 db.user > app/fixtures/users.json

## Other data

    docker-compose exec api bash 
    ./manage.py dumpdata --indent 4 --exclude auth --exclude contenttypes --exclude wagtailcore.GroupCollectionPermission --exclude sessions --exclude wagtailcore --exclude db.user > db/fixtures/initial_data.json


# pylint

    docker-compose exec api bash
    pylint --load-plugins pylint_django --django-settings-module=your.app.settings.test api app db

# Tests

    docker-compose exec api bash
    ./manage.py test --settings=app.settings.test
