import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus
from api.schema import schema
from db.models import Branch, Benefit, Employee, Company, JobPosition


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
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer",
        }
    }
    '''

    variables_step_1_base_invalid_first_name = {
        "step1": {
            "firstName": "",
            "lastName": "Doe",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer"
        }
    }

    variables_step_1_base_invalid_last_name = {
        "step1": {
            "firstName": "Rick",
            "lastName": "",
            "uid": "CHE-000.000.000",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer"
        }
    }

    variables_step_1_base_invalid_uid = {
        "step1": {
            "firstName": "Rick",
            "lastName": "Doe",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer"
        }
    }

    variables_step_1_base_invalid_street = {
        "step1": {
            "firstName": "Rick",
            "lastName": "Doe",
            "street": "",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer"
        }
    }

    variables_step_1_base_invalid_zip = {
        "step1": {
            "firstName": "Rick",
            "lastName": "Doe",
            "street": "ZooStreet",
            "zip": "",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": "Trainer"
        }
    }

    variables_step_1_base_invalid_city = {
        "step1": {
            "firstName": "Rick",
            "lastName": "Doe",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "",
            "phone": "+41791234567",
            "role": "Trainer"
        }
    }

    variables_step_1_base_invalid_phone = {
        "step1": {
            "firstName": "Rick",
            "lastName": "Doe",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "",
            "role": "Trainer"
        }
    }

    variables_step_1_base_invalid_role = {
        "step1": {
            "firstName": "Rick",
            "lastName": "Doe",
            "street": "ZooStreet",
            "zip": "1337",
            "city": "ZooTown",
            "phone": "+41791234567",
            "role": ""
        }
    }

    variables_step_2_base = {
        "step2": {
            "website": "www.google.com",
            "description": "A cool company",
            "services": "creating cool stuff",
            "memberItStGallen": "true"
        }
    }

    variables_step_2_base_invalid_website = {
        "step2": {
            "website": "no valid",
            "description": "A cool company",
            "services": "creating cool stuff",
            "memberItStGallen": "true"
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

    variables_step_2_base_invalid_too_long_description = {
        "step2": {
            "website": "google.com",
            "description": "a" * 1001,
            "services": "",
            "memberItStGallen": "False"
        }
    }

    variables_step_3_base = {
        "step3": {
            "jobPosition": [{"id": 1}],
            "benefits": [{"id": 1, "icon": "doge"}, {"id": 2}],
        }
    }

    def setUp(self):
        self.company = Company.objects.create(uid='CHE-999.999.999', name='Doe Unlimited', zip='0000', city='DoeCity')
        self.company.save()
        self.user = get_user_model().objects.create(
            username='john@doe.com',
            email='john@doe.com',
            type='company',
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
            icon='doge'
        )

        self.benefit = Benefit.objects.create(
            id=2,
            icon='sleep'
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

    def test_company_step_1_valid_base(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base, 1,
                                                 'companyProfileStep1')
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '1337')
        self.assertEqual(company.street, 'ZooStreet')
        self.assertEqual(company.city, 'ZooTown')
        self.assertEqual(company.phone, '+41791234567')
        self.assertEqual(user.employee.role, 'Trainer')

    def test_company_step_1_invalid_first_name(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_first_name, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_1_invalid_last_name(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_last_name, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_1_invalid_uid(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_uid, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_1_invalid_street(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_street, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_1_invalid_city(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_city, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_1_invalid_zip(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_zip, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_1_invalid_phone(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_phone, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_1_invalid_role(self):
        self._test_and_get_step_response_content(self.query_step_1, self.variables_step_1_base_invalid_role, 1,
                                                 'companyProfileStep1', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
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

    def test_company_step_2_invalid_website(self):
        self._test_and_get_step_response_content(self.query_step_2, self.variables_step_2_base_invalid_website, 2,
                                                 'companyProfileStep2', False)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(company.name, 'Doe Unlimited')
        self.assertEqual(company.zip, '0000')
        self.assertEqual(company.city, 'DoeCity')

    def test_company_step_2_invalid_member(self):
        self._test_and_get_step_response_content(self.query_step_2, self.variables_step_2_base_invalid_member, 2,
                                                 'companyProfileStep2', True)
        user = get_user_model().objects.get(pk=self.user.pk)
        company = user.company
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
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
