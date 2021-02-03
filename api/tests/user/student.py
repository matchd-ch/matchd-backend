import json

from django.contrib.auth import get_user_model
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus

from api.schema import schema
from db.models import Student


class StudentGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='john@doe.com',
            email='john@doe.com',
            type='student'
        )
        self.user.set_password('asdf1234$')
        self.user.save()

        Student.objects.create(user=self.user, mobile='+41771234568')

        user_status = UserStatus.objects.get(user=self.user)
        user_status.verified = True
        user_status.save()

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
              me {
                username,
                verified,
                firstName,
                lastName,
                profileStep,
                state
                type
                student {
                    mobile
                }
              }
            }
            '''
        )

        content = json.loads(response.content)

        if success:
            self.assertResponseNoErrors(response)
            self.assertEqual(content['data'].get('me').get('username'), 'john@doe.com')
            self.assertEqual(content['data'].get('me').get('state'), 'INCOMPLETE')
            self.assertEqual(content['data'].get('me').get('profileStep'), 1)
            self.assertEqual(content['data'].get('me').get('type'), 'STUDENT')
            self.assertEqual(content['data'].get('me').get('student').get('mobile'), '+41771234568')
        else:
            self.assertResponseHasErrors(response)
            self.assertIsNone(content['data'].get('me'))

    def test_me(self):
        self._login()
        self._test_me()

    def test_me_without_login(self):
        self._test_me(False)

    def test_profile_step_6_without_login(self):
        response = self.query(
            '''
            mutation StudentProfileMutation($step6: StudentProfileStep6Input) {
              studentProfileStep6(step6: $step6) {
                success,
                errors
              }
            }
            ''', variables={
                'step6': {
                    'state': 'anonymous2'
                }
            }

        )

        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIsNone(content['data'].get('studentProfileStep6'))

    def test_profile_step_6_with_invalid_step(self):
        self._login()
        response = self.query(
            '''
            mutation StudentProfileMutation($step6: StudentProfileStep6Input) {
              studentProfileStep6(step6: $step6) {
                success,
                errors
              }
            }
            ''', variables={
                'step6': {
                    'state': 'anonymous2'
                }
            }

        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertIn('profileStep', content['data'].get('studentProfileStep6').get('errors'))

    def test_profile_step_6_with_invalid_state(self):
        self._login()
        self.user.profile_step = 6
        self.user.save()
        response = self.query(
            '''
            mutation StudentProfileMutation($step6: StudentProfileStep6Input) {
              studentProfileStep6(step6: $step6) {
                success,
                errors
              }
            }
            ''', variables={
                'step6': {
                    'state': 'anonymous2'
                }
            }
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertIn('state', content['data'].get('studentProfileStep6').get('errors'))

    def test_profile_step_6(self):
        self._login()
        self.user.profile_step = 6
        self.user.save()
        response = self.query(
            '''
            mutation StudentProfileMutation($step6: StudentProfileStep6Input) {
              studentProfileStep6(step6: $step6) {
                success,
                errors
              }
            }
            ''', variables={
                'step6': {
                    'state': 'anonymous'
                }
            }
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertTrue(content['data'].get('studentProfileStep6').get('success'))
        self.assertIsNone(content['data'].get('studentProfileStep6').get('errors'))

        # reload user
        user = get_user_model().objects.get(pk=self.user.pk)

        self.assertEqual(user.state, 'anonymous')
        self.assertEqual(user.profile_step, 7)
