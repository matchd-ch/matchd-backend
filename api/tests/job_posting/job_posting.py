import json
from datetime import datetime

from django.contrib.auth import get_user_model
from graphql_auth.models import UserStatus

from api.tests.base import BaseGraphQLTestCase
from db.models import JobOption, JobOptionMode, Company, UserState, JobPosting, Skill, Expectation, Language, \
    LanguageLevel, Branch, JobPostingState


# pylint: disable=C0303
# pylint: disable=R0913
# pylint: disable=R0902
class JobPostingGraphQLTestCase(BaseGraphQLTestCase):

    query_step_1 = '''
    mutation JobPostingMutation($step1: JobPostingInputStep1!) {
      jobPostingStep1(step1: $step1) {
        success,
        errors,
        jobPostingId
      }
    }
    '''

    variables_step_1 = {
      'step1': {
        'description': 'Beschreibung',
        'jobOption': {'id': 1},
        'branch': {'id': 1},
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
            'branch': {'id': 999},
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
            'branch': {'id': 1},
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
            'branch': {'id': 1},
            'workload': 'Workload',
            'jobFromDate': '03.2020',
            'jobToDate': '04.2020',
            'url': None
        }
    }

    query_step_2 = '''
        mutation JobPostingMutation($step2: JobPostingInputStep2!) {
          jobPostingStep2(step2: $step2) {
            success,
            errors,
            jobPostingId
          }
        }
        '''

    variables_step_2 = {
      'step2': {
        'id': 1,
        'expectations': [{'id': 1}],
        'skills': [{'id': 1}],
        'languages': [{'language': 1, 'languageLevel': 1}, {'language': 2, 'languageLevel': 1}]
      }
    }

    variables_step_2_invalid = {
        'step2': {
            'id': 1,
            'expectations': [{'id': 999}],
            'skills': [{'id': 999}],
            'languages': [{'language': 999, 'languageLevel': 999}]
        }
    }

    query_step_3 = '''
    mutation JobPostingMutation($step3: JobPostingInputStep3!) {
      jobPostingStep3(step3: $step3) {
        success,
        errors,
        jobPostingId
      }
    }
    '''

    variables_step_3 = {
      'step3': {
        'id': 1,
        'state': 'PUBLIC'
      }
    }

    def setUp(self):
        self.date_range_option = JobOption.objects.create(name='Date range', mode=JobOptionMode.DATE_RANGE, id=1)
        self.date_from_option = JobOption.objects.create(name='Date from', mode=JobOptionMode.DATE_FROM, id=2)

        self.skill = Skill.objects.create(id=1, name='Test')
        self.expectation = Expectation.objects.create(id=1, name='Test')
        self.branch = Branch.objects.create(id=1, name='Test')

        self.language = Language.objects.create(id=1, name='Test', short_list=True)
        self.language2 = Language.objects.create(id=2, name='Test2', short_list=False)
        self.language_level = LanguageLevel.objects.create(id=1, description='Test')

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

        self.job_posting = JobPosting.objects.create(
            id=1,
            company=self.company,
            job_option=self.date_range_option,
            job_from_date=datetime.now(),
            branch=self.branch
        )

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

    def _test_job_posting(self, query, variables, key, success=True, expected_errors=None):
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, 200)
        if success:
            self.assertTrue(content['data'].get(key).get('success'))
        else:
            self.assertFalse(content['data'].get(key).get('success'))
            if expected_errors is not None:
                for expected_error in expected_errors:
                    self.assertIn(expected_error, content['data'].get(key).get('errors'))
        return content

    def _test_job_posting_without_login(self, query, variables):
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIsNone(content['data'].get('jobPostingStep1'))

    def _test_get_job_posting(self, job_posting_id):
        response = self.query('''
        query {  
          jobPosting(id: %s) {
            id
            description
            jobOption {
              id
              name
              mode
            }
            branch {
              id
              name
            }
            workload
            jobFromDate
            jobToDate
            formStep
            url
            expectations {
              id
              name
            }
            skills {
              id
              name
            }
            languages {
              language {
                id
                name
              }
              languageLevel {
                id
                description
              }
            }
          }
        }
        ''' % str(job_posting_id))
        self.assertResponseNoErrors(response)
        return json.loads(response.content)

    def test_job_posting_step_1_without_login(self):
        self._test_job_posting_without_login(self.query_step_1, self.variables_step_1)

    def test_job_posting_step_1(self):
        self._login('john@doe.com')
        content = self._test_job_posting(self.query_step_1, self.variables_step_1, 'jobPostingStep1')

        job_posting_id = content.get('data').get('jobPostingStep1').get('jobPostingId')
        content = self._test_get_job_posting(job_posting_id)
        job_posting = content.get('data').get('jobPosting')

        self.assertEqual('Beschreibung', job_posting.get('description'))
        self.assertEqual('Arbeitspensum', job_posting.get('workload'))
        self.assertEqual('2021-03-01', job_posting.get('jobFromDate'))
        self.assertEqual('2021-08-01', job_posting.get('jobToDate'))
        self.assertEqual('http://www.google.ch', job_posting.get('url'))
        job_option = job_posting.get('jobOption')
        self.assertEqual('1', job_option.get('id'))
        branch = job_posting.get('branch')
        self.assertEqual('1', branch.get('id'))

    def test_job_posting_step_1_invalid_data(self):
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_1, self.variables_step_1_invalid_data, 'jobPostingStep1', False,
                               ['description', 'jobOption', 'jobFromDate', 'branch'])

    def test_job_posting_step_1_invalid_date_range(self):
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_1, self.variables_step_1_invalid_date_range, 'jobPostingStep1', False,
                               ['jobToDate'])

    def test_job_posting_step_2(self):
        self.job_posting.form_step = 3
        self.job_posting.save()
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_2, self.variables_step_2, 'jobPostingStep2')

        content = self._test_get_job_posting(1)
        job_posting = content.get('data').get('jobPosting')

        expectations = job_posting.get('expectations')
        self.assertEqual(1, len(expectations))
        skills = job_posting.get('skills')
        self.assertEqual(1, len(skills))
        languages = job_posting.get('languages')
        self.assertEqual(1, len(languages))

        self.job_posting = JobPosting.objects.get(pk=1)

        self.assertEqual(JobPostingState.DRAFT, self.job_posting.state)
        self.assertEqual(3, self.job_posting.form_step)

    def test_job_posting_step_2_invalid_data(self):
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_2, self.variables_step_2_invalid, 'jobPostingStep2', False,
                               ['expectations', 'skills'])

    def test_job_posting_step_3(self):
        self.job_posting.form_step = 3
        self.job_posting.save()
        self._login('john@doe.com')
        self._test_job_posting(self.query_step_3, self.variables_step_3, 'jobPostingStep3')

        self.job_posting = JobPosting.objects.get(pk=1)

        self.assertEqual(JobPostingState.PUBLIC, self.job_posting.state)
        self.assertEqual(4, self.job_posting.form_step)
