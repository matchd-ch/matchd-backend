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

# Test Accounts

## Registered / Verified users


| Type | Username | Password | Nickname |
|---|---|---|---|
| Company | company-not-verified@matchd.lo | asdf1234$ | - |
| Company | company-step-1@matchd.lo | asdf1234$ | - |
| Company | company-step-2@matchd.lo | asdf1234$ | - |
| Company | company-step-3@matchd.lo | asdf1234$ | - |
| Company | company-step-4@matchd.lo | asdf1234$ | - |
| Company | company-public@matchd.lo | asdf1234$ | - |
| Company | liip@matchd.lo | asdf1234$ | - |
| University | university-not-verified@matchd.lo | asdf1234$ | - |
| University | university-step-1@matchd.lo | asdf1234$ | - |
| University | university-step-2@matchd.lo | asdf1234$ | - |
| University | university-step-3@matchd.lo | asdf1234$ | - |
| University | university-public@matchd.lo | asdf1234$ | - |
| Student | student-not-verified@matchd.lo | asdf1234$ | - |
| Student | student-step-1@matchd.lo | asdf1234$ | - |
| Student | student-step-2@matchd.lo | asdf1234$ | - |
| Student | student-step-3@matchd.lo | asdf1234$ | - |
| Student | student-step-4@matchd.lo | asdf1234$ | - |
| Student | student-step-5@matchd.lo | asdf1234$ | - |
| Student | student-step-6@matchd.lo | asdf1234$ | - |
| Student | student-public@matchd.lo | asdf1234$ | - |
| Student | student-anonymous@matchd.lo | asdf1234$ | - |

## Accounts with complete profiles

| Type | Username | Password | Nickname | Status |
|---|---|---|---|---|
| Student | student-1@matchd.lo | asdf1234$ | melissa.cianciolo | public |
| Student | student-2@matchd.lo | asdf1234$ | andy.jackson | public |
| Student | student-3@matchd.lo | asdf1234$ | talia.hart | public |
| Student | student-4@matchd.lo | asdf1234$ | kevin.graves | public |
| Student | student-5@matchd.lo | asdf1234$ | timothy.wilson | public |
| Student | student-6@matchd.lo | asdf1234$ | charlie.jencks | public |
| Student | student-7@matchd.lo | asdf1234$ | mark.avery | public |
| Student | student-8@matchd.lo | asdf1234$ | misty.hernandez | public |
| Student | student-9@matchd.lo | asdf1234$ | mary.polite | public |
| Student | student-10@matchd.lo | asdf1234$ | jessica.salazar | public |
| Student | student-11@matchd.lo | asdf1234$ | grete.weber | public |
| Student | student-12@matchd.lo | asdf1234$ | franz.haas | public |
| Student | student-13@matchd.lo | asdf1234$ | amala.volk | public |
| Student | student-14@matchd.lo | asdf1234$ | emil.schaefer | anonymous |
| Student | student-15@matchd.lo | asdf1234$ | waldo.wegener | public |
| Student | student-16@matchd.lo | asdf1234$ | heinz.kraus | public |
| Student | student-17@matchd.lo | asdf1234$ | wilfried.vogt | public |
| Student | student-18@matchd.lo | asdf1234$ | emeline.fabel | public |
| Student | student-19@matchd.lo | asdf1234$ | ima.richter | anonymous |
| Student | student-20@matchd.lo | asdf1234$ | uschi.mayer | public |
| Company | company-1-1@matchd.lo | asdf1234$ | - | public |
| Company | company-1-2@matchd.lo | asdf1234$ | - | public |
| Company | company-2-1@matchd.lo | asdf1234$ | - | public |
| Company | company-2-2@matchd.lo | asdf1234$ | - | public |
| Company | company-3-1@matchd.lo | asdf1234$ | - | public |
| Company | company-3-2@matchd.lo | asdf1234$ | - | public |
| Company | company-4-1@matchd.lo | asdf1234$ | - | public |
| Company | company-4-2@matchd.lo | asdf1234$ | - | public |
| Company | company-5-1@matchd.lo | asdf1234$ | - | public |
| Company | company-5-2@matchd.lo | asdf1234$ | - | public |
| Company | company-6-1@matchd.lo | asdf1234$ | - | public |
| Company | company-6-2@matchd.lo | asdf1234$ | - | public |
| Company | company-7-1@matchd.lo | asdf1234$ | - | public |
| Company | company-7-2@matchd.lo | asdf1234$ | - | public |
| Company | company-8-1@matchd.lo | asdf1234$ | - | public |
| Company | company-8-2@matchd.lo | asdf1234$ | - | public |
| Company | company-9-1@matchd.lo | asdf1234$ | - | public |
| Company | company-9-2@matchd.lo | asdf1234$ | - | public |
| Company | company-10-1@matchd.lo | asdf1234$ | - | public |
| Company | company-10-2@matchd.lo | asdf1234$ | - | public |
| University | company-11-1@matchd.lo | asdf1234$ | - | public |
| University | company-11-2@matchd.lo | asdf1234$ | - | public |
| University | company-12-1@matchd.lo | asdf1234$ | - | public |
| University | company-12-2@matchd.lo | asdf1234$ | - | public |
| University | company-13-1@matchd.lo | asdf1234$ | - | public |
| University | company-13-2@matchd.lo | asdf1234$ | - | public |
| University | company-14-1@matchd.lo | asdf1234$ | - | public |
| University | company-14-2@matchd.lo | asdf1234$ | - | public |
| University | company-15-1@matchd.lo | asdf1234$ | - | public |
| University | company-15-2@matchd.lo | asdf1234$ | - | public |
| University | company-16-1@matchd.lo | asdf1234$ | - | public |
| University | company-16-2@matchd.lo | asdf1234$ | - | public |
| University | company-17-1@matchd.lo | asdf1234$ | - | public |
| University | company-17-2@matchd.lo | asdf1234$ | - | public |
| University | company-18-1@matchd.lo | asdf1234$ | - | public |
| University | company-18-2@matchd.lo | asdf1234$ | - | public |
| University | company-19-1@matchd.lo | asdf1234$ | - | public |
| University | company-19-2@matchd.lo | asdf1234$ | - | public |
| University | company-20-1@matchd.lo | asdf1234$ | - | public |
| University | company-20-2@matchd.lo | asdf1234$ | - | public |

# Dump Fixtures

    docker-compose exec api bash 
    ./manage.py dumpdata --indent 4 --exclude auth --exclude contenttypes --exclude wagtailcore.GroupCollectionPermission --exclude sessions --exclude wagtailcore --exclude refresh_token.refreshtoken --exclude db.skill --exclude db.language --exclude db.languagelevel --exclude db.branch --exclude db.benefit --exclude db.expectation --exclude db.faqcategory --exclude db.softskill --exclude db.userrequest --exclude db.joboption > db/fixtures/initial_data.json

# Zip / City

Download xls file from here: https://postleitzahlenschweiz.ch/tabelle/

Copy the file to api/data/data.xlsx and run the following command:

    pip install pandas
    cd api/data
    python xlsx_to_json.py

# Testing

## pylint

    docker-compose exec api bash
    pylint --load-plugins pylint_django --django-settings-module=app.settings.test api app db

## Tests

    docker-compose exec api bash
    ./manage.py test --settings=app.settings.test
