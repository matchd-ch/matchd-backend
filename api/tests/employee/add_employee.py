import json

from django.contrib.auth import get_user_model
from graphql_auth.models import UserStatus

from api.tests.base import BaseGraphQLTestCase
from db.models import Company, UserState, Employee


class AddEmployeeGraphQLTestCase(BaseGraphQLTestCase):

    def setUp(self):
        self.company = Company.objects.create(uid='CHE-000.000.000', name='Doe Unlimited', zip='0000', city='DoeCity',
                                              slug='doe-unlimited')

        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            username='john@doe.com',
            email='john@doe.com',
            type='company',
            company=self.company
        )
        self.user.set_password('asdf1234$')
        self.user.state = UserState.PUBLIC
        self.user.save()

        self.employee = Employee.objects.create(
            id=1,
            role='Test',
            user=self.user
        )

        user_status = UserStatus.objects.get(user=self.user)
        user_status.verified = True
        user_status.save()

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

    def _test_employees(self, num_employees):
        response = self.query('''
                query {
                    me {
                        company {
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
                                    state
                                }
                            }
                        }
                    }
                }
                ''')
        content = json.loads(response.content)
        self.assertEqual(len(content['data'].get('me').get('company').get('employees')), num_employees)

    def _add_employee(self, email):
        response = self.query('''
        mutation AddEmployeeMutation($addEmployee: AddEmployeeInput!) {
          addEmployee(addEmployee: $addEmployee) {
            success,
            errors,
            employee {
              id
              role
              user {
                firstName
                lastName
                email
                username
              }
            }
          }
        }
        ''', variables={
            'addEmployee': {
                'firstName': 'Test',
                'lastName': 'Test',
                'role': 'Test',
                'email': email
              }
            }
        )
        content = json.loads(response.content)
        self.assertTrue(content.get('data').get('addEmployee').get('success'))

    def test_add_employee(self):
        self._login('john@doe.com')
        self._test_employees(1)
        self._add_employee('mock9@mock.com')
        self._test_employees(2)
