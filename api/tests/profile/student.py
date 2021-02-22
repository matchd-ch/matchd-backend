import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus
from api.schema import schema
from db.models import Student, Skill, Language, LanguageLevel


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

    variables_step_4_base = {
            "step4": {
                "skills": [{"id": 1}],
                "languages": [{"language": 1, "languageLevel": 1}]
            }
    }

    variables_step_4_skill_invalid = {
            "step4": {
                "skills": [{"id": 0}],
                "languages": [{"language": 1, "languageLevel": 1}]
            }
    }

    variables_step_4_hobbies = {
            "step4": {
                "skills": [{"id": 1}],
                "hobbies": [{"name": "TV"}],
                "languages": [{"language": 1, "languageLevel": 1}]
            }
    }

    variables_step_4_hobbies_no_name = {
        "step4": {
            "skills": [{"id": 1}],
            "hobbies": [{"name": ""}],
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }

    variables_step_4_hobbies_update = {
        "step4": {
            "skills": [{"id": 1}],
            "hobbies": [{"id": 1, "name": "gamen"}],
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }

    variables_step_4_hobbies_duplicated = {
        "step4": {
            "skills": [{"id": 1}],
            "hobbies": [{"id": 1}, {"name": "TV"}],
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }

    variables_step_4_language_invalid = {
        "step4": {
            "skills": [{"id": 1}],
            "languages": [{"language": 0, "languageLevel": 1}]
        }
    }

    variables_step_4_multiple_language = {
        "step4": {
            "skills": [{"id": 1}],
            "languages": [{"language": 1, "languageLevel": 1}, {"language": 2, "languageLevel": 2}]
        }
    }

    variables_step_4_duplicated_language = {
        "step4": {
            "skills": [{"id": 1}],
            "languages": [{"language": 1, "languageLevel": 1}, {"language": 1, "languageLevel": 1}]
        }
    }

    variables_step_4_distinction = {
        "step4": {
            "skills": [{"id": 1}],
            "distinction": "valid Text",
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }
    variables_step_4_distinction_update = {
        "step4": {
            "skills": [{"id": 1}],
            "distinction": "updated Text",
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }

    variables_step_4_distinction_too_long_text = {
        "step4": {
            "skills": [{"id": 1}],
            "distinction": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget "
                           "dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, "
                           "nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, "
                           "sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, "
                           "vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, "
                           "justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. "
                           "Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, "
                           "porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, "
                           "viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque "
                           "rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies "
                           "nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, "
                           "sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Noooooo",
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }

    variables_step_4_online_projects = {
        "step4": {
            "skills": [{"id": 1}],
            "onlineProjects": [{"url": "google.com"}],
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }

    variables_step_4_online_projects_invalid = {
        "step4": {
            "skills": [{"id": 1}],
            "onlineProjects": [{"url": "invalid url "}],
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }
    variables_step_4_online_projects_duplicated = {
        "step4": {
            "skills": [{"id": 1}],
            "onlineProjects": [{"id": 1}, {"url": "google.com"}],
            "languages": [{"language": 1, "languageLevel": 1}]
        }
    }

    def setUp(self):
        self.student = get_user_model().objects.create(
            username='jane@doe.com',
            email='jane@doe.com',
            type='student'
        )
        self.student.set_password('asdf1234$')
        self.student.profile_step = 4
        self.student.save()

        Student.objects.create(user=self.student, mobile='+41791234567')

        user_status = UserStatus.objects.get(user=self.student)
        user_status.verified = True
        user_status.save()

        self.skill = Skill.objects.create(
            id=1,
            name='php'
        )

        self.language = Language.objects.create(
            id=1,
            name='Deutsch'
        )

        self.language = Language.objects.create(
            id=2,
            name='Englisch'
        )

        self.language_level = LanguageLevel.objects.create(
            id=1,
            level='A1'
        )

        self.language_level = LanguageLevel.objects.create(
            id=2,
            level='A2'
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

    def test_profile_step_4_valid_base(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_base)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.skills.all()[0].name, 'php')
        self.assertEqual(profile.languages.all()[0].language.name, 'Deutsch')
        self.assertEqual(profile.languages.all()[0].language_level.level, 'A1')
        self.assertEqual(profile.skills.all().count(), 1)

    def test_profile_step_4_invalid_skill(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_skill_invalid, False)

    def test_profile_step_4_valid_hobbies(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.skills.all()[0].name, 'php')
        self.assertEqual(profile.hobbies.all().count(), 1)

    def test_profile_step_4_valid_hobbies_no_name(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies_no_name, False)

    def test_profile_step_4_valid_hobbies_update(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies)
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies_update)

    def test_profile_step_4_valid_distinction(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_distinction)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.distinction, 'valid Text')

    def test_profile_step_4_invalid_languages(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_language_invalid, False)

    def test_profile_step_4_valid_multiple_languages(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_multiple_language)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.languages.all()[0].language.name, 'Deutsch')
        self.assertEqual(profile.languages.all()[1].language.name, 'Englisch')
        self.assertEqual(profile.languages.all()[0].language_level.level, 'A1')
        self.assertEqual(profile.languages.all()[1].language_level.level, 'A2')
        self.assertEqual(profile.languages.count(), 2)

    def test_profile_step_4_valid_online_projects(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_online_projects)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.online_projects.all()[0].url, 'http://google.com')
        self.assertEqual(profile.online_projects.all().count(), 1)

    def test_profile_step_4_invalid_online_projects(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_online_projects_invalid,
                                                 False)

    def test_profile_step_4_valid_duplicated_languages(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_duplicated_language)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.languages.all()[0].language.name, 'Deutsch')
        self.assertEqual(profile.languages.all()[0].language_level.level, 'A1')
        self.assertEqual(profile.languages.count(), 1)

    def test_profile_step_4_valid_duplicated_hobbies(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies)
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_hobbies_duplicated)

        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.hobbies.all()[0].name, 'TV')
        self.assertEqual(profile.hobbies.all().count(), 1)

    def test_profile_step_4_valid_duplicated_online_projects(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_online_projects)
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_online_projects_duplicated)

        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.online_projects.all()[0].url, 'http://google.com')
        self.assertEqual(profile.online_projects.all().count(), 1)

    def test_profile_step_4_valid_base_but_not_logged_in(self):
        response = self.query(self.query_step_4, variables=self.variables_step_4_base)
        self.assertResponseHasErrors(response)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.skills.all().count(), 0)
        self.assertEqual(profile.languages.all().count(), 0)

    def test_profile_step_4_valid_hobbies_but_not_logged_in(self):
        response = self.query(self.query_step_4, variables=self.variables_step_4_hobbies)
        self.assertResponseHasErrors(response)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.hobbies.all().count(), 0)

    def test_profile_step_4_valid_distinction_but_not_logged_in(self):
        response = self.query(self.query_step_4, variables=self.variables_step_4_distinction)
        self.assertResponseHasErrors(response)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.distinction, "")

    def test_profile_step_4_valid_online_projects_but_not_logged_in(self):
        response = self.query(self.query_step_4, variables=self.variables_step_4_online_projects)
        self.assertResponseHasErrors(response)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.online_projects.all().count(), 0)

    def test_profile_step_4_update_distinction(self):
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_distinction)
        self._test_and_get_step_response_content(self.query_step_4, self.variables_step_4_distinction_update)
        user = get_user_model().objects.get(pk=self.student.pk)

        profile = user.student
        self.assertEqual(profile.distinction, 'updated Text')

    def test_profile_step_4_too_long_distinction(self):
        self._login()
        response = self.query(self.query_step_4, variables=self.variables_step_4_distinction_too_long_text)
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content['data'].get('studentProfileStep4').get('success'))
        self.assertIsNotNone(content['data'].get('studentProfileStep4').get('errors'))
        self.assertEqual(content['data'].get('studentProfileStep4').get('errors').get('distinction')[0].get('code'),
                         'max_length')

        user = get_user_model().objects.get(pk=self.student.pk)
        profile = user.student
        self.assertEqual(profile.distinction, '')
