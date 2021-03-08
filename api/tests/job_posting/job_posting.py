import json
from django.contrib.auth import get_user_model
from graphql_auth.models import UserStatus

from api.tests.base import BaseGraphQLTestCase
from db.models import JobOption, JobOptionMode, Company, UserState


class JobPostingGraphQLTestCase(BaseGraphQLTestCase):

    query_step_1 = '''
    mutation JobPostingMutation($step1: JobPostingInputStep1!) {
      jobPostingStep1(step1: $step1) {
        success,
        errors
      }
    }
    '''

    variables_step_1 = {
      'step1': {
        'description': 'Beschreibung',
        'jobOption': {'id': 1},
        'workload': 'Arbeitspensum',
        'jobFromDate': '03.2021',
        'jobToDate': '08.2021',
        'url': 'www.google.ch'
      }
    }

    variables_step_1_invalid_data = {
        'step1': {
            'description': '',
            'jobOption': {'id': 999},
            'workload': '',
            'jobFromDate': '',
            'jobToDate': '',
            'url': None
        }
    }

    variables_step_1_invalid_date_range = {
        'step1': {
            'description': 'Description',
            'jobOption': {'id': 1},
            'workload': 'Workload',
            'jobFromDate': '03.2020',
            'jobToDate': '01.2020',
            'url': None
        }
    }

    variables_step_1_invalid_pdf_url = {
        'step1': {
            'description': 'Description',
            'jobOption': {'id': 1},
            'workload': 'Workload',
            'jobFromDate': '03.2020',
            'jobToDate': '04.2020',
            'url': None
        }
    }

    def setUp(self):
        self.date_range_option = JobOption.objects.create(name='Date range', mode=JobOptionMode.DATE_RANGE, id=1)
        self.date_from_option = JobOption.objects.create(name='Date from', mode=JobOptionMode.DATE_FROM, id=2)

        self.company = Company.objects.create(uid='CHE-000.000.000', name='Doe Unlimited', zip='0000', city='DoeCity')

        self.employee = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            username='john@doe.com',
            email='john@doe.com',
            type='company',
            company=self.company
        )
        self.employee.set_password('asdf1234$')
        self.employee.state = UserState.PUBLIC
        self.employee.save()

        user_status = UserStatus.objects.get(user=self.employee)
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

    def _test_job_posting(self, query, variables, success=True, expected_errors=None):
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, 200)
        if success:
            self.assertTrue(content['data'].get('jobPostingStep1').get('success'))
        else:
            self.assertFalse(content['data'].get('jobPostingStep1').get('success'))
            if expected_errors is not None:
                for expected_error in expected_errors:
                    self.assertIn(expected_error, content['data'].get('jobPostingStep1').get('errors'))

    def _test_job_posting_without_login(self, query, variables):
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIsNone(content['data'].get('jobPostingStep1'))

    def test_job_posting_step_1_without_login(self):
        self._test_job_posting_without_login(self.query_step_1, self.variables_step_1)

    def test_job_posting_step_1(self):
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_1, self.variables_step_1)

    def test_job_posting_step_1_invalid_data(self):
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_1, self.variables_step_1_invalid_data, False,
                               ['description', 'jobOption', 'workload', 'jobFromDate'])

    def test_job_posting_step_1_invalid_date_range(self):
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_1, self.variables_step_1_invalid_date_range, False, ['jobToDate'])
