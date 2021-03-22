import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from graphene_django.utils import GraphQLTestCase
from graphql_auth.models import UserStatus

from api.schema import schema
from db.models import Student, AttachmentKey, Company, ProfileState
from db.models.attachment import get_config_for_key

# pylint: disable=W0612
# pylint: disable=R0913


def get_image(extension='jpg'):
    image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'data', f'image.{extension}')
    return open(image_path, 'rb').read()


def get_video(extension='mp4'):
    image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'data', f'video.{extension}')
    return open(image_path, 'rb').read()


def get_document(extension='pdf'):
    image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'data', f'document.{extension}')
    return open(image_path, 'rb').read()


def get_range_for_key(key):
    config = get_config_for_key(key)
    max_files = config.get('max_files')
    return range(0, max_files - 1)


def camel_case(value):
    output = ''.join(x for x in value.title() if x.isalnum())
    return output[0].lower() + output[1:]


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

        self.student_profile = Student.objects.create(user=self.student, mobile='+41771234568')

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

    def _test_attachments(self, key=AttachmentKey.STUDENT_AVATAR, num_entries=0, mime_types=None, success=True):
        response = self.query('''
        {
          studentAvatar: attachments (key:STUDENT_AVATAR) {
            id
            url
            mimeType
            fileSize
            fileName
          }
          
          studentDocuments: attachments (key:STUDENT_DOCUMENTS) {
            id
            url
            mimeType
            fileSize
            fileName
          }
          
          companyAvatar: attachments (key:COMPANY_AVATAR) {
            id
            url
            mimeType
            fileSize
            fileName
          }
          
          companyDocuments: attachments (key:COMPANY_DOCUMENTS) {
            id
            url
            mimeType
            fileSize
            fileName
          }
        }
        ''')
        if success:
            self.assertResponseNoErrors(response)
        else:
            self.assertResponseHasErrors(response)

        key = camel_case(key)
        content = json.loads(response.content)
        data = content.get('data')

        if num_entries > 0:
            self.assertEqual(len(data.get(key)), num_entries)
            if mime_types is not None:
                index = 0
                for mime_type in mime_types:
                    self.assertEqual(data.get(key)[index].get('mimeType'), mime_type)
                    index += 1

    def _test_user_attachments(self, user_id, key, num_entries):
        response = self.query('''
        {
          studentAvatar: attachments (key:STUDENT_AVATAR, userId: %s) {
            id
            url
            mimeType
            fileSize
            fileName
          }

          studentDocuments: attachments (key:STUDENT_DOCUMENTS, userId: %s) {
            id
            url
            mimeType
            fileSize
            fileName
          }

          companyAvatar: attachments (key:COMPANY_AVATAR, userId: %s) {
            id
            url
            mimeType
            fileSize
            fileName
          }

          companyDocuments: attachments (key:COMPANY_DOCUMENTS, userId: %s) {
            id
            url
            mimeType
            fileSize
            fileName
          }
        }
        ''' % (user_id, user_id, user_id, user_id))

        key = camel_case(key)
        content = json.loads(response.content)
        data = content.get('data')
        self.assertEqual(len(data.get(key)), num_entries)

    def _test_company_attachments(self, company_slug, key, num_entries):
        response = self.query('''
        {
          studentAvatar: attachments (key:STUDENT_AVATAR, slug: "%s") {
            id
            url
            mimeType
            fileSize
            fileName
          }

          studentDocuments: attachments (key:STUDENT_DOCUMENTS, slug: "%s") {
            id
            url
            mimeType
            fileSize
            fileName
          }

          companyAvatar: attachments (key:COMPANY_AVATAR, slug: "%s") {
            id
            url
            mimeType
            fileSize
            fileName
          }

          companyDocuments: attachments (key:COMPANY_DOCUMENTS, slug: "%s") {
            id
            url
            mimeType
            fileSize
            fileName
          }
        }
        ''' % (company_slug, company_slug, company_slug, company_slug))

        key = camel_case(key)
        content = json.loads(response.content)
        data = content.get('data')
        self.assertEqual(len(data.get(key)), num_entries)

    def test_upload_without_login(self):
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type='image/jpeg')
        self._test_upload_without_login(AttachmentKey.STUDENT_AVATAR, file)
        self._test_attachments(success=False)

    def test_upload_student_avatar(self):
        mime_type = 'image/jpeg'
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type=mime_type)
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_AVATAR, file)
        # test max files
        mime_types = [mime_type]
        for i in get_range_for_key(AttachmentKey.STUDENT_AVATAR):
            self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_AVATAR, file)
            mime_types.append(mime_type)
        # too many files
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_AVATAR, file, False, ['key'])
        self._test_attachments(num_entries=len(mime_types), mime_types=mime_types, key=AttachmentKey.STUDENT_AVATAR)

    def test_upload_student_with_company_key(self):
        mime_type = 'image/jpeg'
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type=mime_type)
        self._test_upload_with_login('john@doe.com', AttachmentKey.COMPANY_AVATAR, file, False, ['key'])
        self._test_attachments(key=AttachmentKey.COMPANY_AVATAR)

    def test_upload_company_avatar(self):
        mime_type = 'image/jpeg'
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type=mime_type)
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_AVATAR, file)
        # test max files
        mime_types = [mime_type]
        for i in get_range_for_key(AttachmentKey.COMPANY_AVATAR):
            self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_AVATAR, file)
            mime_types.append(mime_type)
        # too many files
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_AVATAR, file, False, ['key'])
        self._test_attachments(num_entries=len(mime_types), mime_types=mime_types, key=AttachmentKey.COMPANY_AVATAR)

    def test_upload_company_with_student_key(self):
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type='image/jpeg')
        self._test_upload_with_login('john2@doe.com', AttachmentKey.STUDENT_AVATAR, file, False, ['key'])
        self._test_attachments(key=AttachmentKey.STUDENT_AVATAR)

    def test_upload_student_documents(self):
        mime_type = 'application/pdf'
        file = SimpleUploadedFile(name='document.pdf', content=get_document(), content_type=mime_type)
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_DOCUMENTS, file)
        # test max files
        mime_types = [mime_type]
        for i in get_range_for_key(AttachmentKey.STUDENT_DOCUMENTS):
            file.seek(0)
            self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_DOCUMENTS, file)
            mime_types.append(mime_type)
        # too many files
        file.seek(0)
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_DOCUMENTS, file, False, ['key'])
        self._test_attachments(num_entries=len(mime_types), mime_types=mime_types, key=AttachmentKey.STUDENT_DOCUMENTS)

    def test_upload_company_documents(self):
        mime_type = 'application/pdf'
        file = SimpleUploadedFile(name='document.pdf', content=get_document(), content_type=mime_type)
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_DOCUMENTS, file)
        # test max files
        mime_types = [mime_type]
        for i in get_range_for_key(AttachmentKey.COMPANY_DOCUMENTS):
            file.seek(0)
            self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_DOCUMENTS, file)
            mime_types.append(mime_type)
        # too many files
        file.seek(0)
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_DOCUMENTS, file, False, ['key'])
        self._test_attachments(num_entries=len(mime_types), mime_types=mime_types, key=AttachmentKey.COMPANY_DOCUMENTS)

    def test_upload_student_video(self):
        mime_type = 'video/mp4'
        file = SimpleUploadedFile(name='video.mp4', content=get_video(), content_type=mime_type)
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_DOCUMENTS, file)
        # test max files
        mime_types = [mime_type]
        for i in get_range_for_key(AttachmentKey.STUDENT_DOCUMENTS):
            file.seek(0)
            self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_DOCUMENTS, file)
            mime_types.append(mime_type)
        # too many files
        file.seek(0)
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_DOCUMENTS, file, False, ['key'])
        self._test_attachments(num_entries=len(mime_types), mime_types=mime_types, key=AttachmentKey.STUDENT_DOCUMENTS)

    def test_upload_company_video(self):
        mime_type = 'video/mp4'
        file = SimpleUploadedFile(name='video.mp4', content=get_video(), content_type=mime_type)
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_DOCUMENTS, file)
        # test max files
        mime_types = [mime_type]
        for i in get_range_for_key(AttachmentKey.COMPANY_DOCUMENTS):
            file.seek(0)
            self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_DOCUMENTS, file)
            mime_types.append(mime_type)
        # too many files
        file.seek(0)
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_DOCUMENTS, file, False, ['key'])
        self._test_attachments(num_entries=len(mime_types), mime_types=mime_types, key=AttachmentKey.COMPANY_DOCUMENTS)

    def test_company_has_no_access_to_student_attachments(self):
        mime_type = 'image/jpeg'
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type=mime_type)
        self._test_upload_with_login('john@doe.com', AttachmentKey.STUDENT_AVATAR, file)
        self._test_attachments(num_entries=1, mime_types=[mime_type], key=AttachmentKey.STUDENT_AVATAR)

        # incomplete profile
        self.student.state = ProfileState.INCOMPLETE
        self.student.save()

        # login as company
        self._login('john2@doe.com')
        # attachments not accessible
        self._test_user_attachments(self.student.id, AttachmentKey.STUDENT_AVATAR, 0)

        # anonymous profile
        self.student.state = ProfileState.ANONYMOUS
        self.student.save()

        # attachments not accessible
        self._test_user_attachments(self.student.id, AttachmentKey.STUDENT_AVATAR, 0)

        # public profile
        self.student.state = ProfileState.PUBLIC
        self.student.save()

        # attachments accessible
        self._test_user_attachments(self.student.id, AttachmentKey.STUDENT_AVATAR, 1)

    def test_student_has_access_to_company_attachments(self):
        mime_type = 'image/jpeg'
        file = SimpleUploadedFile(name='image.jpg', content=get_image(extension='jpg'), content_type=mime_type)
        self._test_upload_with_login('john2@doe.com', AttachmentKey.COMPANY_AVATAR, file)

        # incomplete profile
        self.employee.state = ProfileState.INCOMPLETE
        self.employee.save()

        # login as student
        self._login('john@doe.com')
        # attachments not accessible
        self._test_company_attachments(self.company.slug, AttachmentKey.COMPANY_AVATAR, 0)

        # anonymous profile
        self.employee.state = ProfileState.ANONYMOUS
        self.employee.save()

        # attachments accessible
        self._test_company_attachments(self.company.slug, AttachmentKey.COMPANY_AVATAR, 1)

        # public profile
        self.employee.state = ProfileState.PUBLIC
        self.employee.save()

        # attachments accessible
        self._test_company_attachments(self.company.slug, AttachmentKey.COMPANY_AVATAR, 1)
