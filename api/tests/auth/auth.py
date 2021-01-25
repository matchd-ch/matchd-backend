import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from graphene_django.utils import GraphQLTestCase


from api.schema import schema
from db.models import UserType, Student


class JWLTokenGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def _check_model_entries(self, model, expected_entries=0):
        num_entries = model.objects.all().count()
        self.assertEqual(expected_entries, num_entries)

    def _register(self):
        self._check_model_entries(get_user_model())
        self._check_model_entries(Student)

        response = self.query(
            '''
            mutation RegisterStudent {
              registerStudent(
                email: "rudolph@doe.com",
                username: "rudolph@doe.com",
                password1: "asdf1234$",
                password2:"asdf1234$",
                firstName: "Rudolph",
                lastName: "Doe",
                student: {
                    mobileNumber: "+41791234567"
                }) {
                success
                errors
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content.get('data').get('registerStudent').get('success'))
        self.assertIsNone(content.get('data').get('registerStudent').get('errors'))

        self._check_model_entries(get_user_model(), 1)
        self._check_model_entries(Student, 1)

        user = get_user_model().objects.get(email='rudolph@doe.com')
        self.assertEqual(user.type, UserType.STUDENT)


    def _get_and_test_activation_token(self, activation_email):
        activation_url = activation_email.body.split('\n')[-2]
        verification_path = settings.GRAPHQL_AUTH.get('ACTIVATION_PATH_ON_EMAIL')
        self.assertIn(f'https://{settings.FRONTEND_URL}/{verification_path}/', activation_url)
        return activation_url.split('/')[-1]

    def _verify_account(self, token):
        response = self.query(
            '''
            mutation VerifyAccount($token: String! ) {
              verifyAccount(token: $token) {
                success
                errors
              }
            }
            ''', variables={'token': token}
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content['data'].get('verifyAccount').get('success'))

    def _get_and_test_auth_token(self):
        response = self.query(
            '''
            mutation TokenAuth {
                tokenAuth(username: "rudolph@doe.com", password: "asdf1234$") {
                    success,
                    errors,
                    unarchiving,
                    token,
                    unarchiving,
                    refreshToken,
                    user {
                        email,
                        username,
                    }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content['data'].get('tokenAuth').get('success'))
        self.assertIsNotNone(content['data'].get('tokenAuth').get('token'))


    def test_registration_student_with_auth_token(self):
        self._register()

        self.assertTemplateUsed('api/email/activation/body.html')
        self.assertTemplateUsed('api/email/activation/subject.txt')

        activation_email = mail.outbox[0]
        self.assertIn('rudolph@doe.com', activation_email.recipients())
        self.assertIn(settings.EMAIL_SUBJECT_PREFIX, activation_email.subject)
        self.assertIn('MATCHD Registration Student', activation_email.subject)

        activation_token = self._get_and_test_activation_token(activation_email)
        self.assertIsNotNone(activation_token)
        self._verify_account(activation_token)

        self._get_and_test_auth_token()
