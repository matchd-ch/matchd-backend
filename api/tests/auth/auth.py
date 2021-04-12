import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import ProfileType, Student


class AuthGraphQLTestCase(GraphQLTestCase):
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
                type: "student",
                student: {
                    mobile: "+41791234567"
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
        self.assertEqual(user.type, ProfileType.STUDENT)

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

    def _get_and_test_auth_token(self, success=True):
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

        if success:
            self.assertTrue(content['data'].get('tokenAuth').get('success'))
            self.assertIsNotNone(content['data'].get('tokenAuth').get('token'))
        else:
            self.assertFalse(content['data'].get('tokenAuth').get('success'))
            self.assertIsNone(content['data'].get('tokenAuth').get('token'))

    def _get_and_test_auth_token_with_wrong_password(self):
        response = self.query(
            '''
            mutation TokenAuth {
                tokenAuth(username: "rudolph@doe.com", password: "WrongPassword") {
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
        return content

    def _logout(self):
        response = self.query(
            '''
            mutation Logout {
              logout
            }
            '''
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertTrue(content['data'].get('logout'))
        self.assertEqual(response.cookies['JWT'].value, '')

    def test_auth_token_without_activation(self):
        self._register()
        self._get_and_test_auth_token(success=False)

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

        self._get_and_test_auth_token(success=True)

    def test_auth_token_wrong_password(self):
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

        content = self._get_and_test_auth_token_with_wrong_password()
        self.assertFalse(content['data'].get('tokenAuth').get('success'))
        self.assertIsNone(content['data'].get('tokenAuth').get('token'))

    def _test_send_password_reset_email(self, success):
        response = self.query(
            '''
           mutation sendPasswordResetEmail{
            sendPasswordResetEmail(
                email: "rudolph@doe.com"
            ) {
            success,
            errors
            }
        }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        if success:
            self.assertTrue(content['data'].get('sendPasswordResetEmail').get('success'))
        else:
            self.assertFalse(content['data'].get('sendPasswordResetEmail').get('success'))

    def _get_password_reset_token(self, reset_email):
        reset_url = reset_email.body.split('\n')[-2]
        verification_path = settings.GRAPHQL_AUTH.get('PASSWORD_RESET_PATH_ON_EMAIL')
        self.assertIn(f'https://{settings.FRONTEND_URL}/{verification_path}/', reset_url)
        return reset_url.split('/')[-1]

    def _test_reset_password(self, token, password1, password2, success):
        response = self.query(
            '''
           mutation PasswordReset($token: String!, $password1: String!, $password2: String!,  ) {
              passwordReset(
                token: $token,
                newPassword1: $password1,
                newPassword2: $password2
              ) {
                success,
                errors
              }
            }
            ''', variables={'token': token, 'password1': password1, 'password2': password2}
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertIsNotNone(content)

        if success:
            self.assertTrue(content['data'].get('passwordReset').get('success'))
        else:
            self.assertFalse(content['data'].get('passwordReset').get('success'))

    def _password_reset(self, password1, password2, success):
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

        self._test_send_password_reset_email(True)

        reset_email = mail.outbox[1]
        password_reset_token = self._get_password_reset_token(reset_email)
        self.assertIsNotNone(password_reset_token)

        self._test_reset_password(password_reset_token, password1, password2, success)

    def test_password_reset(self):
        self._password_reset('superStrongPassword1!', 'superStrongPassword1!', True)

    def test_password_reset_with_weak_password(self):
        self._password_reset('weakPassword', 'weakPassword', False)

    def test_password_reset_with_miss_matched(self):
        self._password_reset('weakPassword', 'weakPasswordButNotTheSame', False)

    def test_reset_token_with_wrong_token(self):
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

        self._test_send_password_reset_email(True)

        self._test_reset_password('wrongToken', 'superStrongPassword1!', 'superStrongPassword1!', False)

    def _verify_password_reset_token(self, token):
        response = self.query(
            '''
           query($token: String!){
            verifyPasswordResetToken(token: $token)
            }
            ''', variables={'token': token}
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        return content

    def test_verify_password_reset_token(self):
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

        self._test_send_password_reset_email(True)

        reset_email = mail.outbox[1]
        self._get_password_reset_token(reset_email)

    def test_logout(self):
        self._register()
        activation_email = mail.outbox[0]
        token = self._get_and_test_activation_token(activation_email)
        self._verify_account(token)
        self._get_and_test_auth_token()
        self._logout()