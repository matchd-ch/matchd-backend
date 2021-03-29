import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus

from api.schema import schema
from db.models import ProfileType, Student


class StudentRegistrationGraphQLTestCase(GraphQLTestCase):
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

    def _register_twice(self):
        self._check_model_entries(get_user_model(), 1)
        self._check_model_entries(Student, 1)

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
                }
              ) {
                success
                errors
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content['data'].get('registerStudent').get('success'))
        self.assertIn('username', content['data'].get('registerStudent').get('errors'))
        self.assertEqual(content['data'].get('registerStudent').get('errors').get('username')[0].get('code'), 'unique')

        self._check_model_entries(get_user_model(), 1)
        self._check_model_entries(Student, 1)

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

    def _register_with_weak_password(self, password, expected_code):
        response = self.query(
            '''
            mutation RegisterStudent {
              registerStudent(
                email: "rudolph@doe.com",
                username: "rudolph@doe.com",
                password1: "%s",
                password2:"%s",
                firstName: "Rudolph",
                lastName: "Doe",
                type: "student",
                student: {
                    mobile: "+41791234567"
                }
              ) {
                success
                errors
              }
            }
            ''' % (password, password)
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content['data'].get('registerStudent').get('success'))
        self.assertIn('password2', content['data'].get('registerStudent').get('errors'))
        self.assertEqual(
            content['data'].get('registerStudent').get('errors').get('password2')[0].get('code'),
            expected_code
        )

    def test_registration_student_with_account_verification(self):
        self._register()
        self._register_twice()

        self.assertTemplateUsed('api/email/activation/body.html')
        self.assertTemplateUsed('api/email/activation/subject.txt')

        activation_email = mail.outbox[0]
        self.assertIn('rudolph@doe.com', activation_email.recipients())
        self.assertIn(settings.EMAIL_SUBJECT_PREFIX, activation_email.subject)
        self.assertIn('MATCHD Registration Student', activation_email.subject)

        activation_token = self._get_and_test_activation_token(activation_email)
        self.assertIsNotNone(activation_token)

        user = get_user_model().objects.get(email='rudolph@doe.com')
        user_status = UserStatus.objects.get(user=user)

        self.assertFalse(user_status.verified)
        self._verify_account(activation_token)

        user_status = UserStatus.objects.get(user=user)
        self.assertTrue(user_status.verified)

    def test_registration_with_invalid_email(self):
        response = self.query(
            '''
            mutation RegisterStudent {
              registerStudent(
                email: "invalid",
                username: "invalid",
                password1: "asdf1234$",
                password2:"asdf1234$",
                firstName: "Rudolph",
                lastName: "Doe",
                type: "student",
                student: {
                    mobile: "+41791234567"
                }
              ) {
                success
                errors
              }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content['data'].get('registerStudent').get('success'))
        self.assertIn('email', content['data'].get('registerStudent').get('errors'))
        self.assertEqual(content['data'].get('registerStudent').get('errors').get('email')[0].get('code'), 'invalid')

    def test_register_with_weak_password_too_short(self):
        self._register_with_weak_password('1234567', 'password_too_short')

    def test_register_with_weak_password_no_digits(self):
        self._register_with_weak_password('veryComplicatedPassword$ButStillWeak', 'no_digit')

    def test_register_with_weak_password_no_letters(self):
        self._register_with_weak_password('$$$$$//////()()()()$1234567', 'no_letter')

    def test_register_with_weak_password_no_specialchars(self):
        self._register_with_weak_password('veryComplicatedPasswordButStillWeak123456789', 'no_specialchars')

    def test_register_without_first_name_and_last_name(self):
        response = self.query(
            '''
          mutation RegisterStudent {
              registerStudent(
                email: "rudolph@doe.com",
                username: "rudolph@doe.com",
                password1: "asdf1234$",
                password2:"asdf1234$",
                firstName: "",
                lastName: "",
                type: "student",
                student: {
                    mobile: "+41791234567"
                }
              ) {
                success
                errors
              }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content['data'].get('registerStudent').get('success'))
        self.assertIn('firstName', content['data'].get('registerStudent').get('errors'))
        self.assertIn('lastName', content['data'].get('registerStudent').get('errors'))

    def test_register_without_student_data(self):
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
                type: "student"
              ) {
                success
                errors
              }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content['data'].get('registerStudent').get('success'))

    def test_register_with_wrong_mobile_number(self):
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
                    mobile: "+417611"
                }
              ) {
                success
                errors
              }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content['data'].get('registerStudent').get('success'))
        self.assertIn('mobile', content['data'].get('registerStudent').get('errors'))
