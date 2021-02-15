import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus
from api.schema import schema
from db.models import Student, Skill


class StudentGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    query_step_4 = '''
                mutation StudentProfileMutation($step4: StudentProfileInputStep4!) {
                    studentProfileStep4(step4: $step4) {
                        success,
                       errors
                    }
                }
                '''

    variables_step_4_skills = {
            "step4": {
                "skills": [{"id": 1}],
                "languages": [{"language": 1, "languageLevel": 1}],
            }
    }

    variables_step_4_skills_invalid = {
            "step4": {
                "skills": [{"id": 0}],
                "languages": [{"language": 1, "languageLevel": 1}],
            }
    }

    variables_step_4_hobbies = {
            "step4": {
                "skills": [{"id": 1}],
                "hobbies": [{"name": "TV"}],
                "languages": [{"language": 1, "languageLevel": 1}],
            }
    }

    variables_step_4_hobbies_no_name = {
        "step4": {
            "skills": [{"id": 1}],
            "hobbies": [{"name": ""}],
            "languages": [{"language": 1, "languageLevel": 1}],
        }
    }

    variables_step_4_hobbies_update = {
        "step4": {
            "skills": [{"id": 1}],
            "hobbies": [{"id": 1, "name": "gamen"}],
            "languages": [{"language": 1, "languageLevel": 1}],
        }
    }

    def setUp(self):
        self.student = get_user_model().objects.create(
            username='jane@doe.com',
            email='jane@doe.com',
            type='student'
        )
        self.student.set_password('asdf1234$')
        self.student.save()

        Student.objects.create(user=self.student, mobile='+41791234567')

        user_status = UserStatus.objects.get(user=self.student)
        user_status.verified = True
        user_status.save()

        self.skill = Skill.objects.create(
            id=1,
            name='php'
        )

    def _test_and_get_step_response_content(self, query, variables, success=True):
        self._login()
        response = self.query(query, variables=variables)
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        if success:
            self.assertTrue(content['data'].get('studentProfileStep4').get('success'))
            self.assertIsNone(content['data'].get('studentProfileStep4').get('errors'))
        else:
            self.assertFalse(content['data'].get('studentProfileStep4').get('success'))
            self.assertIsNotNone(content['data'].get('studentProfileStep4').get('errors'))
        return content

    def _login(self):
        response = self.query(
            '''
            mutation TokenAuth {
                tokenAuth(username: "jane@doe.com", password: "asdf1234$") {
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

    def test_profile_step_4_valid_skills(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_skills)

    def test_profile_step_4_invalid_skills(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_skills_invalid, False)

    def test_profile_step_4_valid_hobbies(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies)

    def test_profile_step_4_valid_hobbies_no_name(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies_no_name, False)

    def test_profile_step_4_valid_hobbies_update(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies)
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies_update)
