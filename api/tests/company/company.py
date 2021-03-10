import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus
from api.schema import schema
from db.models import Branch, Benefit, Employee, Company, JobPosition


# pylint:disable=R0913
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
    query_step_2 = '''
    mutation CompanyProfileMutation($step2: CompanyProfileInputStep2!) {
        companyProfileStep2(step2: $step2) {
            success,
            errors
        }
    }
    '''
    query_step_3 = '''
    mutation CompanyProfileMutation($step3: CompanyProfileInputStep3!) {
        companyProfileStep3(step3: $step3) {
            success,
            errors
        }
    }
    '''

    variables_step_1_base = '''
        {
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
    '''

    variables_step_2_base = {
        "step2": {
            "website": "www.google.com",
            "description": "A cool company",
            "services": "creating cool stuff",
            "memberItStGallen": True
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

    variables_step_3_base = {
        "step3": {
            "jobPositions": [{"id": 1}],
            "benefits": [{"id": 1, "icon": "doge"}, {"id": 2}],
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

    variables_step_2_invalid = {
        "step2": {
            "website": "",
            "description": "",
            "services": "",
            "memberItStGallen": ""
        }
    }

    variables_step_3_invalid = {
        "step3": {
            "jobPositions": [{"id": 0}],
            "benefits": [{"id": 99, "icon": "not valid"}],
        }
    }

    def setUp(self):
        self.company = Company.objects.create(uid='CHE-999.999.999', name='Doe Unlimited', zip='0000', city='DoeCity')
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
        self.user.profile_step = 1
        self.user.save()

        user_status = UserStatus.objects.get(user=self.user)
        user_status.verified = True
        user_status.save()

        self.employee = Employee.objects.create(
            role='Trainer',
            user=get_user_model().objects.get(pk=self.user.pk)
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

    def _test_and_get_step_response_content(self, query, variables, step, error, success=True):
        self._login()
        self.user.profile_step = step
        self.user.save()
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
        self._login()
        self.user.profile_step = step
        self.user.save()

        response = self.query(query, variables=variables)
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        errors = content['data'].get(error_key).get('errors')
        for expected_error in expected_errors:
            self.assertIn(expected_error, errors)

    def _login(self):
        response = self.query(
            '''
            mutation TokenAuth {
                tokenAuth(username: "john@doe.com", password: "asdf1234$") {
                    success,
                    errors,
                    token
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content['data'].get('tokenAuth').get('success'))
        self.assertIsNotNone(content['data'].get('tokenAuth').get('token'))

    def _test_me(self, success=True):
        response = self.query(
            '''
            query {
                me{
                    id,
                    username,
                    email,
                    type,
                    firstName,
                    lastName,
                    state,
                    profileStep,
                    employee{
                        id,
                        role,
                    }
                    company{
                        uid,
                        name,
                        zip,
                        city,
                        street,
                        phone,
                        website,
                        description,
                        services,
                        memberItStGallen,
                    benefits{
                        id,
                        icon
                    }
                    jobPositions{
                        id,
                        name
                    }
                }
            }
            '''
        )

        content = json.loads(response.content)

        if success:
            self.assertResponseNoErrors(response)
            self.assertEqual(content['data'].get('me').get('username'), 'john@doe.com')
            self.assertEqual(content['data'].get('me').get('first_name'), 'Johnny')
            self.assertEqual(content['data'].get('me').get('last_name'), 'Test')
            self.assertEqual(content['data'].get('me').get('state'), 'INCOMPLETE')
            self.assertEqual(content['data'].get('me').get('profileStep'), 1)
            self.assertEqual(content['data'].get('me').get('type'), 'COMPANY')
            self.assertEqual(content['data'].get('me').get('company').get('mobile'), '+41791234567')

        else:
            self.assertResponseHasErrors(response)
            self.assertIsNone(content['data'].get('me'))

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
                                     ['website'])
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
