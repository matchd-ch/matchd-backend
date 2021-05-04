import json
import os
import shutil

import pytest
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from db.models import Attachment, Image, AttachmentKey


def attachments_by_slug_query(slug):
    return '''
    {
        companyAvatar: attachments (key:COMPANY_AVATAR, slug: "%s") {
            id
            url
            mimeType
            fileSize
            fileName
          }
          
        companyAvatarFallback: attachments (key:COMPANY_AVATAR_FALLBACK, slug: "%s") {
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
        
        studentAvatar: attachments (key:STUDENT_AVATAR, slug: "%s") {
            id
            url
            mimeType
            fileSize
            fileName
        }
        
        studentAvatarFallback: attachments (key:STUDENT_AVATAR_FALLBACK, slug: "%s") {
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
    }
    ''' % (slug, slug, slug, slug, slug, slug)


@pytest.fixture
def query_attachments_for_slug(execute):
    def closure(user, slug):
        return execute(attachments_by_slug_query(slug), **{'user': user})
    return closure


def upload_mutation(key):
    return '''
    mutation {
      upload(file: Upload, key: %s) {
        success
        errors
      }
    }
    ''' % key.upper()


@pytest.fixture
def upload(default_password):
    def closure(user, key, file):
        query = upload_mutation(key)
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
        client = Client()
        client.login(username=user.username, password=default_password)
        response = client.post('/graphql/', data=data)
        content = json.loads(response.content)
        return content.get('data'), content.get('errors')
    return closure


def delete_attachment_mutation(attachment_id):
    return '''
    mutation {
      deleteAttachment(id:%i) {
        success
        errors
      }
    }
    ''' % attachment_id


@pytest.fixture
def file_image_jpg():
    mime_type = 'image/jpeg'
    image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'fixtures', 'media', 'image.jpg')
    file = open(image_path, 'rb').read()
    return SimpleUploadedFile(name='image.jpg', content=file, content_type=mime_type)


@pytest.fixture
def file_video_mp4():
    mime_type = 'video/mp4'
    image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'fixtures', 'media', 'video.mp4')
    file = open(image_path, 'rb').read()
    return SimpleUploadedFile(name='video.mp4', content=file, content_type=mime_type)


@pytest.fixture
def file_document_pdf():
    mime_type = 'application/pdf'
    image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'fixtures', 'media', 'document.pdf')
    file = open(image_path, 'rb').read()
    return SimpleUploadedFile(name='document.pdf', content=file, content_type=mime_type)


@pytest.fixture
def attachments_for_user():
    def closure(user, key):
        profile_content_type = user.get_profile_content_type()
        profile_id = user.get_profile_id()
        return Attachment.objects.filter(key=key, content_type=profile_content_type, object_id=profile_id)
    return closure


@pytest.fixture
def delete_attachment(execute):
    def closure(user, attachment_id):
        return execute(delete_attachment_mutation(attachment_id), **{'user': user})
    return closure


@pytest.mark.django_db
@pytest.fixture(autouse=True)
def company_fallback_images(user_employee):
    image_content_type = ContentType.objects.get(app_label='db', model='image')

    source_image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'fixtures', 'media', 'image.jpg')
    destination_image_path = os.path.join(settings.MEDIA_ROOT, 'company_image.jpg')
    shutil.copy(source_image_path, destination_image_path)

    image = Image.objects.create(file='company_image.jpg')
    Attachment.objects.create(key=AttachmentKey.COMPANY_AVATAR_FALLBACK, object_id=user_employee.get_profile_id(),
                              content_type=user_employee.get_profile_content_type(), attachment_id=image.id,
                              attachment_type=image_content_type)

    source_image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'fixtures', 'media', 'image.jpg')
    destination_image_path = os.path.join(settings.MEDIA_ROOT, 'company_image_2.jpg')
    shutil.copy(source_image_path, destination_image_path)

    image = Image.objects.create(file='company_image_2.jpg')
    Attachment.objects.create(key=AttachmentKey.COMPANY_AVATAR_FALLBACK, object_id=user_employee.get_profile_id(),
                              content_type=user_employee.get_profile_content_type(), attachment_id=image.id,
                              attachment_type=image_content_type)


@pytest.mark.django_db
@pytest.fixture(autouse=True)
def student_fallback_images(user_student):
    image_content_type = ContentType.objects.get(app_label='db', model='image')

    source_image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'fixtures', 'media', 'image.jpg')
    destination_image_path = os.path.join(settings.MEDIA_ROOT, 'student_image.jpg')
    shutil.copy(source_image_path, destination_image_path)
    image = Image.objects.create(file='student_image.jpg')

    Attachment.objects.create(key=AttachmentKey.COMPANY_AVATAR_FALLBACK, object_id=user_student.get_profile_id(),
                              content_type=user_student.get_profile_content_type(), attachment_id=image.id,
                              attachment_type=image_content_type)

    source_image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'fixtures', 'media', 'image.jpg')
    destination_image_path = os.path.join(settings.MEDIA_ROOT, 'student_image_2.jpg')
    shutil.copy(source_image_path, destination_image_path)
    image = Image.objects.create(file='student_image_2.jpg')

    Attachment.objects.create(key=AttachmentKey.STUDENT_AVATAR_FALLBACK, object_id=user_student.get_profile_id(),
                              content_type=user_student.get_profile_content_type(), attachment_id=image.id,
                              attachment_type=image_content_type)
