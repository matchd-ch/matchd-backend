import json

from django.conf import settings
from django.core import mail
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import UserRequest


class UserRequestGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def _check_user_request_entries(self, expected_entries=0):
        num_entries = UserRequest.objects.all().count()
        self.assertEqual(expected_entries, num_entries)

    def test_user_request(self):
        self._check_user_request_entries()
        variables = {
          'userRequest': {
            'name': 'Jane Doe',
            'email': 'jane@doe.com',
            'message': 'Debug Data Message'
          }
        }
        
        response = self.query(
            '''
            mutation UserRequest($userRequest: UserRequestInput!) {
              userRequest(input: $userRequest) {
                success
                errors
              }
            }
            ''', variables=variables
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content.get('data').get('userRequest').get('success'))
        self.assertIsNone(content.get('data').get('userRequest').get('errors'))

        self._check_user_request_entries(1)

        self.assertTemplateUsed('db/email/user_request/body.html')
        self.assertTemplateUsed('db/email/user_request/body.txt')
        self.assertTemplateUsed('db/email/user_request/subject.txt')

        self.assertTemplateUsed('db/email/user_request_copy/body.html')
        self.assertTemplateUsed('db/email/user_request_copy/body.txt')
        self.assertTemplateUsed('db/email/user_request_copy/subject.txt')

        request_email_copy = mail.outbox[0]
        self.assertIn('jane@doe.com', request_email_copy.recipients())
        self.assertIn('Jane Doe', request_email_copy.body)
        self.assertIn('jane@doe.com', request_email_copy.body)
        self.assertIn('Debug Data Message', request_email_copy.body)
        self.assertIn(settings.EMAIL_SUBJECT_PREFIX, request_email_copy.subject)

        request_email = mail.outbox[1]
        for recipient in settings.USER_REQUEST_FORM_RECIPIENTS:
            self.assertIn(recipient, request_email.recipients())
        self.assertIn('Jane Doe', request_email.body)
        self.assertIn('jane@doe.com', request_email.body)
        self.assertIn('Debug Data Message', request_email.body)
        self.assertIn(settings.EMAIL_SUBJECT_PREFIX, request_email.subject)

    def test_user_request_without_data(self):
        self._check_user_request_entries()
        variables = {
            'userRequest': {
                'name': '',
                'email': '',
                'message': ''
            }
        }

        response = self.query(
            '''
            mutation UserRequest($userRequest: UserRequestInput!) {
              userRequest(input: $userRequest) {
                success
                errors
              }
            }
            ''', variables=variables
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content.get('data').get('userRequest').get('success'))
        self.assertIn('email', content.get('data').get('userRequest').get('errors'))
        self.assertIn('name', content.get('data').get('userRequest').get('errors'))
        self.assertIn('message', content.get('data').get('userRequest').get('errors'))

        self._check_user_request_entries(0)

    def test_user_request_with_invalid_data(self):
        self._check_user_request_entries()
        variables = {
            'userRequest': {
                'name': 'Jane Doe',
                'email': 'invalid_email',
                'message': 'Test Message'
            }
        }

        response = self.query(
            '''
            mutation UserRequest($userRequest: UserRequestInput!) {
              userRequest(input: $userRequest) {
                success
                errors
              }
            }
            ''', variables=variables
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertFalse(content.get('data').get('userRequest').get('success'))
        self.assertIn('email', content.get('data').get('userRequest').get('errors'))
        self.assertEqual(
            'Enter a valid email address.',
            content.get('data').get('userRequest').get('errors').get('email')[0]
        )

        self._check_user_request_entries(0)