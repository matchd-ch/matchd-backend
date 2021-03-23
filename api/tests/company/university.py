import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus
from api.schema import schema
from db.models import Employee, Company, ProfileState, UserType


# pylint:disable=R0913
# pylint:disable=R0902
class UniversityGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    query_step_1 = '''
    mutation UniversityProfileMutation($step1: UniversityProfileInputStep1!) {
        universityProfileStep1(step1: $step1) {
            success,
            errors
        }
    }
    '''

    variables_step_1_valid = {
        "step1": {
            "firstName": "John",
            "lastName": "Doe",
            "name": "Zoo",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer",
            "website": "www.unlimited.ch",
            "topLevelOrganisationWebsite": "www.toplevel.ch",
            "topLevelOrganisationDescription": "Top Level Description"
        }
    }

    variables_step_1_invalid = {
        "step1": {
            "firstName": "",
            "lastName": "",
            "name": "",
            "street": "",
            "zip": "",
            "city": "",
            "phone": "",
            "role": "",
            "website": "",
            "topLevelOrganisationWebsite": "",
            "topLevelOrganisationDescription": ""
        }
    }

    variables_step_1_invalid_data = {
        "step1": {
            "firstName": "John",
            "lastName": "Doe",
            "name": "Zoo",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer",
            "website": "www.unlimited.ch",
            "topLevelOrganisationWebsite": "invalid_url",
            "topLevelOrganisationDescription": 'a' * 1001
        }
    }

    def setUp(self) -> None:
        self.university = Company.objects.create(id=1, name='Doe University', zip='0000', city='DoeCity',
                                                 slug='doe-university', profile_step=1, type=UserType.UNIVERSITY)
        self.university.save()
        self.user = get_user_model().objects.create(
            username='john@doe.com',
            email='john@doe.com',
            type=UserType.UNIVERSITY,
            first_name='Johnny',
            last_name='Test',
            company=self.university
        )
        self.user.set_password('asdf1234$')
        self.user.save()

        user_status = UserStatus.objects.get(user=self.user)
        user_status.verified = True
        user_status.save()

        self.employee = Employee.objects.create(
            role='Trainer',
            user=self.user
        )
        self.employee.save()

    def _test_and_get_step_response_content(self, query, variables, step, error, success=True):
        self._login('john@doe.com')
        # update company, otherwise multi step tests won't work
        self.university = Company.objects.get(pk=self.university.id)
        self.university.profile_step = step
        self.university.save()
        response = self.query(query, variables=variables)

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        if success:
            self.assertTrue(content['data'].get(error).get('success'))
            self.assertIsNone(content['data'].get(error).get('errors'))
        else:
            self.assertFalse(content['data'].get(error).get('success'))
            self.assertIsNotNone(content['data'].get(error).get('errors'))
        return content

    def _test_with_invalid_data(self, step, query, variables, error_key, expected_errors):
        self._login('john@doe.com')
        self.university.profile_step = step
        self.university.save()

        response = self.query(query, variables=variables)
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        errors = content['data'].get(error_key).get('errors')
        for expected_error in expected_errors:
            self.assertIn(expected_error, errors)

    def _login(self, username):
        response = self.query(
            '''
            mutation TokenAuth {
                tokenAuth(username: "%s", password: "asdf1234$") {
                    success,
                    errors,
                    token
                }
            }
            ''' % username
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content['data'].get('tokenAuth').get('success'))
        self.assertIsNotNone(content['data'].get('tokenAuth').get('token'))

    def _logout(self):
        response = self.query(
            '''
            mutation Logout {
              logout
            }
            '''
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertTrue(content['data'].get('logout'))
        self.assertEqual(response.cookies['JWT'].value, '')

    def _test_me(self, success=True):
        response = self.query('''
        query {
            me {
                id
                username
                email
                type
                firstName
                lastName
                company {
                    type
                    name
                    zip
                    city
                    street
                    phone
                    website                
                    state
                    profileStep
                    employees {
                        id
                        role
                        user {
                            id
                            username
                            email
                            type
                            firstName
                            lastName
                        }
                    }
                    topLevelOrganisationDescription
                    topLevelOrganisationWebsite
                }
            }
        }
        ''')
        content = json.loads(response.content)

        if success:
            self.assertResponseNoErrors(response)

            me_data = content['data'].get('me')
            company = me_data.get('company')
            employees = company.get('employees')

            self.assertEqual(me_data.get('username'), 'john@doe.com')
            self.assertEqual(me_data.get('firstName'), 'Johnny')
            self.assertEqual(me_data.get('lastName'), 'Test')
            self.assertEqual(me_data.get('type'), UserType.COMPANY.upper())

            self.assertEqual(employees[0].get('role'), 'Trainer')
            self.assertEqual(employees[0].get('user').get('username'), 'john@doe.com')
            self.assertEqual(employees[0].get('user').get('email'), 'john@doe.com')
            self.assertEqual(employees[0].get('user').get('type'), UserType.COMPANY.upper())
            self.assertEqual(employees[0].get('user').get('firstName'), 'Johnny')
            self.assertEqual(employees[0].get('user').get('lastName'), 'Test')

            self.assertEqual(company.get('state'), ProfileState.INCOMPLETE.upper())
            self.assertEqual(company.get('profileStep'), 1)
        else:
            self.assertResponseHasErrors(response)
            self.assertIsNone(content['data'].get('me'))

    def _test_company_query(self, company_slug, success=True):
        response = self.query(
            '''
            query{
                company(slug:"%s"){
                    id
                    type
                    slug
                    name
                    zip
                    city
                    street
                    phone
                    website                    
                    state
                    profileStep                    
                    employees{
                      id
                      role
                      user{
                        firstName
                        lastName
                        email
                      }
                    }
                    topLevelOrganisationDescription
                    topLevelOrganisationWebsite
                }
            }
            ''' % company_slug
        )

        content = json.loads(response.content)
        if success:
            self.assertResponseNoErrors(response)
            self.assertEqual(content['data'].get('company').get('uid'), 'CHE-999.999.999')
            self.assertEqual(content['data'].get('company').get('name'), 'Zoo')
            self.assertEqual(content['data'].get('company').get('zip'), '1337')
            self.assertEqual(content['data'].get('company').get('city'), 'ZooTown')
            self.assertEqual(content['data'].get('company').get('street'), 'ZooStreet')
            self.assertEqual(content['data'].get('company').get('phone'), '+41791234567')
            self.assertEqual(content['data'].get('company').get('website'), 'http://www.google.com')
            self.assertEqual(content['data'].get('company').get('description'), 'A cool company')
            self.assertEqual(content['data'].get('company').get('services'), 'creating cool stuff')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('user').get('firstName'), 'John')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('user').get('lastName'), 'Doe')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('user').get('email'),
                             'john@doe.com')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('role'), 'Trainer')
        else:
            self.assertResponseHasErrors(response)
            self.assertIsNone(content['data'].get('company'))

    def test_university_step_1_valid_data(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_valid, 1,
                                                 'universityProfileStep1')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(company.name, 'Zoo')
        self.assertEqual(company.zip, '1337')
        self.assertEqual(company.street, 'ZooStreet')
        self.assertEqual(company.city, 'ZooTown')
        self.assertEqual(company.phone, '+41791234567')
        self.assertEqual(company.top_level_organisation_website, 'http://www.toplevel.ch')
        self.assertEqual(company.top_level_organisation_description, 'Top Level Description')
        self.assertEqual(user.employee.role, 'Trainer')

    def test_university_step_1_invalid_data(self):
        self._test_with_invalid_data(1, self.query_step_1, self.variables_step_1_invalid, 'universityProfileStep1',
                                     ['firstName', 'lastName', 'name', 'zip', 'street', 'city', 'phone', 'role'])

        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company

        self.assertEqual(user.first_name, 'Johnny')
        self.assertEqual(user.last_name, 'Test')
        self.assertEqual(company.name, 'Doe University')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_university_step_1_invalid_data_top_level(self):
        self._test_with_invalid_data(1, self.query_step_1, self.variables_step_1_invalid_data, 'universityProfileStep1',
                                     ['topLevelOrganisationDescription', 'topLevelOrganisationWebsite'])

        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company

        self.assertEqual(user.first_name, 'Johnny')
        self.assertEqual(user.last_name, 'Test')
        self.assertEqual(company.name, 'Doe University')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')
