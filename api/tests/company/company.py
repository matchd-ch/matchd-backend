import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus
from api.schema import schema
from db.models import Branch, Benefit, Employee, Company, JobPosition, Student, ProfileState, ProfileType


# pylint:disable=R0913
# pylint:disable=R0902
class CompanyGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    query_step_1 = '''
    mutation CompanyProfileMutation($step1: CompanyProfileInputStep1!) {
        companyProfileStep1(step1: $step1) {
            success,
            errors
        }
    }
    '''

    variables_step_1_base = {
        "step1": {
            "firstName": "John",
            "lastName": "Doe",
            "name": "Zoo",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer"
        }
    }

    variables_step_1_invalid = {
        "step1": {
            "firstName": "",
            "lastName": "",
            "street": "",
            "zip": "",
            "city": "",
            "phone": "",
            "role": ""
        }
    }

    query_step_2 = '''
    mutation CompanyProfileMutation($step2: CompanyProfileInputStep2!) {
        companyProfileStep2(step2: $step2) {
            success,
            errors
        }
    }
    '''

    variables_step_2_base = {
        "step2": {
            "website": "www.google.com",
            "description": "A cool company",
            "services": "creating cool stuff",
            "memberItStGallen": True,
            "branch": {"id": 1}
        }
    }

    variables_step_2_invalid = {
        "step2": {
            "website": "",
            "description": "",
            "services": "",
            "memberItStGallen": "",
            "branch": {"id": 99}
        }
    }

    variables_step_2_base_invalid_member = {
        "step2": {
            "website": "google.com",
            "description": "",
            "services": "",
            "memberItStGallen": ""
        }
    }

    query_step_3 = '''
    mutation CompanyProfileMutation($step3: CompanyProfileInputStep3!) {
        companyProfileStep3(step3: $step3) {
            success,
            errors
        }
    }
    '''

    variables_step_3_base = {
        "step3": {
            "jobPositions": [{"id": 1}],
            "benefits": [{"id": 1, "icon": "doge"}, {"id": 2}],
        }
    }

    variables_step_3_invalid = {
        "step3": {
            "jobPositions": [{"id": 0}],
            "benefits": [{"id": 99, "icon": "not valid"}],
        }
    }

    def setUp(self):
        self.company = Company.objects.create(id=1, uid='CHE-999.999.999', name='Doe Unlimited', zip='0000',
                                              city='DoeCity', slug='doe-unlimited', profile_step=1,
                                              type=ProfileType.COMPANY)
        self.company.save()
        self.user = get_user_model().objects.create(
            username='john@doe.com',
            email='john@doe.com',
            type='company',
            first_name='Johnny',
            last_name='Test',
            company=self.company
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

        self.branch = Branch.objects.create(
            id=1,
            name='software'
        )
        self.branch.save()

        self.benefit = Benefit.objects.create(
            id=1,
            icon='doge',
            name='Doge'
        )
        self.benefit = Benefit.objects.create(
            id=2,
            icon='sleep',
            name='Sleep'
        )

        self.job_position = JobPosition.objects.create(
            id=1,
            name='worker'
        )

        self.student = get_user_model().objects.create(
            username='jane@doe.com',
            email='jane@doe.com',
            type='student'
        )
        self.student.set_password('asdf1234$')
        self.student.save()

        self.student_profile = Student.objects.create(user=self.student, mobile='+41771234568')

        user_status = UserStatus.objects.get(user=self.student)
        user_status.verified = True
        user_status.save()

    def _test_and_get_step_response_content(self, query, variables, step, error, success=True):
        self._login('john@doe.com')
        # update company, otherwise multi step tests won't work
        self.company = Company.objects.get(pk=self.company.id)
        self.company.profile_step = step
        self.company.save()
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
        self.company.profile_step = step
        self.company.save()

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
                    uid
                    type
                    name
                    zip
                    city
                    street
                    phone
                    website
                    description
                    services
                    memberItStGallen
                    state
                    profileStep
                    branch {
                        id
                        name
                    }
                    benefits {
                        id
                        icon
                    }
                    jobPositions {
                        id
                        name
                    }
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
            self.assertEqual(me_data.get('type'), ProfileType.COMPANY.upper())

            self.assertEqual(employees[0].get('role'), 'Trainer')
            self.assertEqual(employees[0].get('user').get('username'), 'john@doe.com')
            self.assertEqual(employees[0].get('user').get('email'), 'john@doe.com')
            self.assertEqual(employees[0].get('user').get('type'), ProfileType.COMPANY.upper())
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
                    uid
                    name
                    zip
                    city
                    street
                    phone
                    website
                    description
                    services
                    state
                    profileStep
                    branch {
                        id
                        name
                    }
                    benefits{
                      id
                      icon
                    }
                    jobPositions{
                      id
                      name
                    }
                    employees{
                      id
                      role
                      user{
                        firstName
                        lastName
                        email
                      }
                    }
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
            self.assertEqual(content['data'].get('company').get('benefits')[0].get('id'), '1')
            self.assertEqual(content['data'].get('company').get('benefits')[0].get('icon'), 'doge')
            self.assertEqual(content['data'].get('company').get('benefits')[1].get('id'), '2')
            self.assertEqual(content['data'].get('company').get('benefits')[1].get('icon'), 'sleep')
            self.assertEqual(content['data'].get('company').get('jobPositions')[0].get('id'), '1')
            self.assertEqual(content['data'].get('company').get('jobPositions')[0].get('name'), 'worker')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('user').get('firstName'), 'John')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('user').get('lastName'), 'Doe')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('user').get('email'),
                             'john@doe.com')
            self.assertEqual(content['data'].get('company').get('employees')[0].get('role'), 'Trainer')
        else:
            self.assertResponseHasErrors(response)
            self.assertIsNone(content['data'].get('company'))

    def test_company_step_1_valid_base(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base, 1,
                                                 'companyProfileStep1')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(company.name, 'Zoo')
        self.assertEqual(company.zip, '1337')
        self.assertEqual(company.street, 'ZooStreet')
        self.assertEqual(company.city, 'ZooTown')
        self.assertEqual(company.phone, '+41791234567')
        self.assertEqual(user.employee.role, 'Trainer')

    def test_company_step_1_invalid_data(self):
        self._test_with_invalid_data(1, self.query_step_1, self.variables_step_1_invalid, 'companyProfileStep1',
                                     ['firstName', 'lastName', 'name', 'zip', 'street', 'city', 'phone', 'role'])

        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company

        self.assertEqual(user.first_name, 'Johnny')
        self.assertEqual(user.last_name, 'Test')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_2_valid_base(self):
        self._test_and_get_step_response_content(self.query_step_2, self.variables_step_2_base, 2,
                                                 'companyProfileStep2')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(company.website, 'http://www.google.com')
        self.assertEqual(company.description, 'A cool company')
        self.assertEqual(company.services, 'creating cool stuff')
        self.assertEqual(company.member_it_st_gallen, True)

    def test_company_step_2_invalid_data(self):
        self._test_with_invalid_data(2, self.query_step_2, self.variables_step_2_invalid, 'companyProfileStep2',
                                     ['website', 'branch'])
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, 'Johnny')
        self.assertEqual(user.last_name, 'Test')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_2_invalid_member(self):
        self._test_and_get_step_response_content(self.query_step_2, self.variables_step_2_base_invalid_member, 2,
                                                 'companyProfileStep2', True)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, 'Johnny')
        self.assertEqual(user.last_name, 'Test')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')
        self.assertEqual(company.member_it_st_gallen, False)

    def test_company_step_3_valid_base(self):
        self._test_and_get_step_response_content(self.query_step_3, self.variables_step_3_base, 3,
                                                 'companyProfileStep3', True)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(company.benefits.all()[0].icon, 'doge')
        self.assertEqual(company.benefits.all()[1].icon, 'sleep')
        self.assertEqual(company.job_positions.all()[0].name, 'worker')

    def test_company_step_3_invalid_data(self):
        self._test_with_invalid_data(3, self.query_step_3, self.variables_step_3_invalid, 'companyProfileStep3',
                                     ['benefits', 'jobPositions'])

    def test_company_query_invalid_company_id(self):
        self._login('john@doe.com')
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base, 1,
                                                 'companyProfileStep1')
        self._test_and_get_step_response_content(self.query_step_2, self.variables_step_2_base, 2,
                                                 'companyProfileStep2')
        self._test_and_get_step_response_content(self.query_step_3, self.variables_step_3_base, 3,
                                                 'companyProfileStep3', True)
        self._test_company_query('a-wrong-slug', False)

    def test_company_query_not_completed(self):
        # company step 1
        self._login('john@doe.com')
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base, 1,
                                                 'companyProfileStep1')

        # company should not be returned for other users
        self._logout()
        self._login('jane@doe.com')
        self._test_company_query('doe-unlimited', False)

        # company step 2
        self._logout()
        self._login('john@doe.com')
        self._test_and_get_step_response_content(self.query_step_2, self.variables_step_2_base, 2,
                                                 'companyProfileStep2')

        # company should still not be returned for other users
        self._logout()
        self._login('jane@doe.com')
        self._test_company_query('doe-unlimited', False)

        # company step 3
        self._logout()
        self._login('john@doe.com')
        self._test_and_get_step_response_content(self.query_step_3, self.variables_step_3_base, 3,
                                                 'companyProfileStep3')

        # company should be returned for other users
        self._logout()
        self._login('jane@doe.com')
        self._test_company_query('doe-unlimited')

    def test_me_company(self):
        self._login('john@doe.com')
        self._test_me(True)
