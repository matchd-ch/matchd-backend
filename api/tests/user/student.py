import json
from datetime import datetime

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus

from api.schema import schema
from db.models import Student, JobOption, JobOptionMode, JobPosition, SoftSkill


# pylint:disable=R0913
# pylint:disable=R0904
class StudentGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    query_step_1 = '''
    mutation StudentProfileMutation($step1: StudentProfileInputStep1!) {
        studentProfileStep1(step1: $step1) {
            success,
            errors
        }
    }
    '''

    variables_step_1 = {
        'step1': {
            'firstName': 'John2',
            'lastName': 'Doe2',
            'street': 'Doestreet 55',
            'zip': '9000',
            'city': 'St. Gallen',
            'dateOfBirth': '01.01.2000',
            'mobile': '+41999999999'
        }
    }

    invalid_variables_step_1 = {
        'step1': {
            'firstName': '',
            'lastName': '',
            'street': '',
            'zip': '',
            'city': '',
            'dateOfBirth': '',
            'mobile': ''
        }
    }

    query_step_2 = '''
    mutation StudentProfileMutation($step2: StudentProfileInputStep2!) {
        studentProfileStep2(step2: $step2) {
            success,
            errors
        }
    }
    '''

    variables_step_2_date_range = '''
    {
        "step2": {
            "jobOption": {"id": 1},
            "jobFromDate": "01.2020",
            "jobToDate": "03.2020",
            "jobPosition": {"id": 1},
            "softSkills": [{"id": 1}]
        }
    }
    '''

    variables_step_2_date_from = '''
    {
        "step2": {
            "jobOption": {"id": 2},
            "jobFromDate": "01.2020",
            "jobToDate": "",
            "jobPosition": {"id": 1},
            "softSkills": [{"id": 1}]
        }
    }
    '''

    invalid_variables_step_2_date_range = '''
    {
        "step2": {
            "jobOption": {
                "id": 1
            },
            "jobFromDate": "01.2020",
            "jobToDate": "",
            "jobPosition": {
                "id": 1
            },
            "softSkills": [{"id": 1}]
        }
    }
    '''

    invalid_variables_step_2_date_from = '''
    {
        "step2": {
            "jobOption": {
                "id": 2
            },
            "jobFromDate": "18.2020",
            "jobToDate": "",
            "jobPosition": {
                "id": 1
            },
            "softSkills": [{"id": 1}]
        }
    }
    '''

    query_step_5 = '''
    mutation StudentProfileMutation($step5: StudentProfileInputStep5!) {
        studentProfileStep5(step5: $step5) {
            success,
            errors,
            nicknameSuggestions
        }
    }
    '''

    variables_step_5 = {
        'step5': {
            'nickname': 'jane_doe'
        }
    }

    invalid_variables_step_5 = {
        'step5': {
            'nickname': ''
        }
    }

    invalid_variables_step_5_nickname = {
        'step5': {
            'nickname': 'john_doe'
        }
    }

    query_step_6 = '''
    mutation StudentProfileMutation($step6: StudentProfileInputStep6!) {
        studentProfileStep6(step6: $step6) {
            success,
            errors
        }
    }
    '''

    variables_step_6 = {
        'step6': {
            'state': 'anonymous'
        }
    }

    invalid_variables_step_6 = {
        'step6': {
            'state': 'anonymous2'
        }
    }

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='john@doe.com',
            email='john@doe.com',
            type='student'
        )
        self.user.set_password('asdf1234$')
        self.user.save()

        self.student = Student.objects.create(user=self.user, mobile='+41771234568')

        user_status = UserStatus.objects.get(user=self.user)
        user_status.verified = True
        user_status.save()

        self.company = get_user_model().objects.create(
            username='john2@doe.com',
            email='john2@doe.com',
            type='company'
        )
        self.company.set_password('asdf1234$')
        self.company.save()

        user_status = UserStatus.objects.get(user=self.company)
        user_status.verified = True
        user_status.save()

        self.student_with_nickname = get_user_model().objects.create(
            username='john3@doe.com',
            email='john3@doe.com',
            type='student'
        )
        self.student_with_nickname.set_password('asdf1234$')
        self.student_with_nickname.save()

        self.soft_skill = SoftSkill.objects.create(
            id=1,
            student='student skill',
            company='company skill'
        )
        self.soft_skill.save()

        Student.objects.create(user=self.student_with_nickname, mobile='+41771234568', nickname='john_doe')

        user_status = UserStatus.objects.get(user=self.student_with_nickname)
        user_status.verified = True
        user_status.save()

        self.date_range_option = JobOption.objects.create(name='Date range', mode=JobOptionMode.DATE_RANGE, id=1)
        self.date_from_option = JobOption.objects.create(name='Date from', mode=JobOptionMode.DATE_FROM, id=2)

        self.job_position = JobPosition.objects.create(name='Job position', id=1)

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

    def _test_me(self, success=True):
        response = self.query(
            '''
            query {
                me {
                    username
                    firstName
                    lastName
                    type
                    student {
                      profileStep
                      state
                      mobile
                      zip
                      street
                      city
                      dateOfBirth
                      nickname
                      schoolName
                      fieldOfStudy
                      graduation
                      distinction
                      skills {
                        id
                        name
                      }
                      hobbies {
                        id
                        name
                      }
                      languages {
                        id
                        language {
                          id
                          name
                        }
                        languageLevel {
                          id
                          level
                          description
                        }
                      }
                      onlineProjects{
                        id
                        url
                      }
                      softSkill{
                        id
                        student
                        company
                      }
                    }
                }
            }
            '''
        )

        content = json.loads(response.content)

        if success:
            self.assertResponseNoErrors(response)
            self.assertEqual(content['data'].get('me').get('username'), 'john@doe.com')
            self.assertEqual(content['data'].get('me').get('type'), 'STUDENT')
            self.assertEqual(content['data'].get('me').get('student').get('mobile'), '+41771234568')
            self.assertEqual(content['data'].get('me').get('student').get('state'), 'INCOMPLETE')
            self.assertEqual(content['data'].get('me').get('student').get('profileStep'), 1)
        else:
            self.assertResponseHasErrors(response)
            self.assertIsNone(content['data'].get('me'))

    def _test_step_without_login(self, query, variables, error_key):
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIsNone(content['data'].get(error_key))

    def _test_step_as_company(self, query, variables, error_key):
        self._login('john2@doe.com')
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertFalse(content['data'].get(error_key).get('success'))
        self.assertIn('type', content['data'].get(error_key).get('errors'))

    def _test_step_with_invalid_step(self, invalid_step, query, variables, error_key):
        self._login('john@doe.com')
        self.student.profile_step = invalid_step
        self.student.save()
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertIn('profileStep', content['data'].get(error_key).get('errors'))

    def _test_step_with_invalid_data(self, step, query, variables, error_key, expected_errors):
        self._login('john@doe.com')
        self.student.profile_step = step
        self.student.save()
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        errors = content['data'].get(error_key).get('errors')
        for expected_error in expected_errors:
            self.assertIn(expected_error, errors)

    def _test_and_get_step_response_content(self, step, query, variables, error_key, success=True):
        self._login('john@doe.com')
        self.student.profile_step = step
        self.student.save()
        response = self.query(query, variables=variables)
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        if success:
            self.assertTrue(content['data'].get(error_key).get('success'))
            self.assertIsNone(content['data'].get(error_key).get('errors'))
        else:
            self.assertFalse(content['data'].get(error_key).get('success'))
            self.assertIsNotNone(content['data'].get(error_key).get('errors'))
        return content

    def test_me(self):
        self._login('john@doe.com')
        self._test_me()

    def test_me_without_login(self):
        self._test_me(False)

    def test_profile_step_1_without_login(self):
        self._test_step_without_login(self.query_step_1, self.variables_step_1, 'studentProfileStep1')

    def test_profile_step_2_without_login(self):
        self._test_step_without_login(self.query_step_2, self.variables_step_2_date_range, 'studentProfileStep2')

    def test_profile_step_5_without_login(self):
        self._test_step_without_login(self.query_step_5, self.variables_step_5, 'studentProfileStep5')

    def test_profile_step_6_without_login(self):
        self._test_step_without_login(self.query_step_6, self.variables_step_6, 'studentProfileStep6')

    def test_profile_step_1_as_company(self):
        self._test_step_as_company(self.query_step_1, self.variables_step_1, 'studentProfileStep1')

    def test_profile_step_2_as_company(self):
        self._test_step_as_company(self.query_step_2, self.variables_step_2_date_range, 'studentProfileStep2')

    def test_profile_step_5_as_company(self):
        self._test_step_as_company(self.query_step_5, self.variables_step_5, 'studentProfileStep5')

    def test_profile_step_6_as_company(self):
        self._test_step_as_company(self.query_step_6, self.variables_step_6, 'studentProfileStep6')

    def test_profile_step_1_with_invalid_step(self):
        self._test_step_with_invalid_step(0, self.query_step_1, self.variables_step_1, 'studentProfileStep1')

    def test_profile_step_2_with_invalid_step(self):
        self._test_step_with_invalid_step(1, self.query_step_2, self.variables_step_2_date_range, 'studentProfileStep2')

    def test_profile_step_5_with_invalid_step(self):
        self._test_step_with_invalid_step(4, self.query_step_5, self.variables_step_5, 'studentProfileStep5')

    def test_profile_step_6_with_invalid_step(self):
        self._test_step_with_invalid_step(5, self.query_step_6, self.variables_step_6, 'studentProfileStep6')

    def test_profile_step_1_with_invalid_data(self):
        self._test_step_with_invalid_data(1, self.query_step_1, self.invalid_variables_step_1, 'studentProfileStep1',
                                          ['firstName', 'lastName', 'dateOfBirth'])

    def test_profile_step_2_with_invalid_data_date_range(self):
        self._test_step_with_invalid_data(2, self.query_step_2, self.invalid_variables_step_2_date_range,
                                          'studentProfileStep2', ['jobToDate'])

    def test_profile_step_2_with_invalid_data_date_from(self):
        self._test_step_with_invalid_data(2, self.query_step_2, self.invalid_variables_step_2_date_from,
                                          'studentProfileStep2', ['jobFromDate'])

    def test_profile_step_5_with_invalid_data(self):
        self._test_step_with_invalid_data(5, self.query_step_5, self.invalid_variables_step_5, 'studentProfileStep5',
                                          ['nickname'])

    def test_profile_step_6_with_invalid_data(self):
        self._test_step_with_invalid_data(6, self.query_step_6, self.invalid_variables_step_6, 'studentProfileStep6',
                                          ['state'])

    def test_profile_step_1(self):
        self._test_and_get_step_response_content(1, self.query_step_1, self.variables_step_1, 'studentProfileStep1')
        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual('John2', user.first_name)
        self.assertEqual('Doe2', user.last_name)

        profile = user.student
        self.assertEqual(profile.street, 'Doestreet 55')
        self.assertEqual(profile.zip, '9000')
        self.assertEqual(profile.city, 'St. Gallen')
        date_of_birth = datetime.strptime('01.01.2000', '%d.%m.%Y').date()
        self.assertEqual(profile.date_of_birth, date_of_birth)
        self.assertEqual(profile.mobile, '+41999999999')
        self.assertEqual(profile.profile_step, 2)

    def test_profile_step_2(self):
        self._test_and_get_step_response_content(2, self.query_step_2, self.variables_step_2, 'studentProfileStep2')
        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)

        profile = user.student
        self.assertEqual(profile.school_name, 'FH Winterthur')
        self.assertEqual(profile.field_of_study, 'Applikationsentwicklung')
        graduation = datetime.strptime('08.2022', '%m.%Y').date()
        self.assertEqual(profile.graduation, graduation)
        self.assertEqual(profile.profile_step, 3)

    def test_profile_step_3_date_range(self):
        self._test_and_get_step_response_content(3, self.query_step_3, self.variables_step_3_date_range,
                                                 'studentProfileStep3')
    def test_profile_step_2_date_range(self):
        self._test_and_get_step_response_content(2, self.query_step_2, self.variables_step_2_date_range,
                                                 'studentProfileStep2')

        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)

        profile = user.student
        self.assertEqual(profile.job_option.id, self.date_range_option.id)
        from_date = datetime.strptime('01.2020', '%m.%Y').date()
        self.assertEqual(profile.job_from_date, from_date)
        to_date = datetime.strptime('03.2020', '%m.%Y').date()
        self.assertEqual(profile.job_to_date, to_date)
        self.assertEqual(profile.job_position.id, self.job_position.id)
        self.assertEqual(profile.profile_step, 4)
        self.assertEqual(profile.soft_skill.all()[0].id, 1)

    def test_profile_step_2_date_from(self):
        self._test_and_get_step_response_content(2, self.query_step_2, self.variables_step_2_date_from,
                                                 'studentProfileStep2')

        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)

        profile = user.student
        self.assertEqual(profile.job_option.id, self.date_from_option.id)
        from_date = datetime.strptime('01.2020', '%m.%Y').date()
        self.assertEqual(profile.job_from_date, from_date)
        self.assertIsNone(profile.job_to_date)
        self.assertEqual(profile.job_position.id, self.job_position.id)
        self.assertEqual(profile.profile_step, 4)
        self.assertEqual(profile.soft_skill.all()[0].id, 1)

    def test_profile_step_5(self):
        self._test_and_get_step_response_content(5, self.query_step_5, self.variables_step_5, 'studentProfileStep5')

        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)
        profile = user.student
        self.assertEqual(profile.nickname, 'jane_doe')
        self.assertEqual(profile.profile_step, 6)

    def test_profile_step_5_with_existing_nickname(self):
        content = self._test_and_get_step_response_content(5, self.query_step_5, self.invalid_variables_step_5_nickname,
                                                           'studentProfileStep5', False)
        errors = content['data'].get('studentProfileStep5').get('errors')
        self.assertIn('nickname', errors)
        self.assertIsNotNone(content['data'].get('studentProfileStep5').get('nicknameSuggestions'))

        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(user.student.profile_step, 5)

    def test_profile_step_6(self):
        self._test_and_get_step_response_content(6, self.query_step_6, self.variables_step_6, 'studentProfileStep6')
        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(user.student.state, 'anonymous')
        self.assertEqual(user.student.profile_step, 7)
