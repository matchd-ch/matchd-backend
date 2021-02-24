import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus

from api.schema import schema
from db.models import Student, AttachmentKey, Company
from db.models.attachment import get_config_for_key


def get_image(extension='jpg'):
    image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'data', f'image.{extension}')
    return open(image_path, 'rb').read()


def get_range_for_key(key):
    config = get_config_for_key(key)
    max_files = config.get('max_files')
    return range(0, max_files - 2)


class AttachmentGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self) -> None:
        self.student = get_user_model().objects.create(
            username='john@doe.com',
            email='john@doe.com',
            type='student'
        )
        self.student.set_password('asdf1234$')
        self.student.save()

        Student.objects.create(user=self.student, mobile='+41771234568')

        user_status = UserStatus.objects.get(user=self.student)
        user_status.verified = True
        user_status.save()

        self.company = Company.objects.create(uid='CHE-000.000.000', name='Doe Unlimited', zip='0000', city='DoeCity')

        self.employee = get_user_model().objects.create(
            username='john2@doe.com',
            email='john2@doe.com',
            type='company',
            company=self.company
        )
        self.employee.set_password('asdf1234$')
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

    def _test_upload(self, upload_key, file):
        query = '''
            mutation {
              upload(file: Upload, key: %s) {
                success
                errors
              }
            }
            ''' % upload_key.upper()

        data = {
            'operations': json.dumps({
                'query': query,
                'variables': {
                    'file': None,
                },
            }),
            '0': file,
            'map': json.dumps({
                '0': ['variables.file'],
            }),
        }

        response = self.client.post(
            '/graphql/',
            data=data
        )
        return response

    def _test_upload_without_login(self, upload_key, file):
        response = self._test_upload(upload_key, file)
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIsNone(content['data'].get('upload'))

    def _test_upload_with_login(self, username, upload_key, file, success=True, expected_errors=None):
        self._login(username)
        response = self._test_upload(upload_key, file)
        content = json.loads(response.content)
        print(content)
        if success:
            self.assertResponseNoErrors(response)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(content['data'].get('upload').get('success'))
        else:
            self.assertResponseNoErrors(response)
            self.assertFalse(content['data'].get('upload').get('success'))
            if expected_errors is not None:
                for expected_error in expected_errors:
                    self.assertIn(expected_error, content['data'].get('upload').get('errors'))

    def test_upload_without_login(self):
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type='image/jpeg')
        self._test_upload_without_login(AttachmentKey.STUDENT_AVATAR, file)

    def test_upload_student_avatar(self):
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type='image/jpeg')
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_AVATAR, file)
        # test max files
        for i in get_range_for_key(AttachmentKey.COMPANY_AVATAR):
            self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_AVATAR, file)
        # too many files
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_AVATAR, file, False, ['key'])

    def test_upload_student_with_company_key(self):
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type='image/jpeg')
        self._test_upload_with_login('john@doe.com', AttachmentKey.COMPANY_AVATAR, file, False, ['key'])

    def test_upload_company_avatar(self):
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type='image/jpeg')
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_AVATAR, file)
        # test max files
        for i in get_range_for_key(AttachmentKey.COMPANY_AVATAR):
            self._test_upload_with_login('john@doe.com', AttachmentKey.COMPANY_AVATAR, file)
        # too many files
        self._test_upload_with_login('john@doe.com', AttachmentKey.COMPANY_AVATAR, file, False, ['key'])

    def test_upload_company_with_student_key(self):
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type='image/jpeg')
        self._test_upload_with_login('john2@doe.com', AttachmentKey.STUDENT_AVATAR, file, False, ['key'])
