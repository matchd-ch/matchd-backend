from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _


class AttachmentKey(models.TextChoices):
    STUDENT_AVATAR = 'student_avatar', _('Student Avatar')
    STUDENT_DOCUMENTS = 'student_documents', _('Student Documents')
    COMPANY_AVATAR = 'company_avatar', _('Company Avatar')
    COMPANY_DOCUMENTS = 'company_documents', _('Company Documents')


class Attachment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='user_type')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    attachment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='attachment_type')
    attachment_id = models.PositiveIntegerField()
    attachment_object = GenericForeignKey('attachment_type', 'attachment_id')

    key = models.CharField(choices=AttachmentKey.choices, max_length=100, blank=False, null=False)


def student_avatar_config():
    return {
        'content_types_configuration': [
            {
                'content_types': settings.USER_UPLOADS_IMAGE_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE
            }
        ],
        'max_files': 1,
        'key': AttachmentKey.STUDENT_AVATAR
    }


def student_documents_config():
    return {
        'content_types_configuration': [
            {
                'content_types': settings.USER_UPLOADS_VIDEO_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_VIDEO_SIZE
            },
            {
                'content_types': settings.USER_UPLOADS_DOCUMENT_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_DOCUMENT_SIZE
            },
            {
                'content_types': settings.USER_UPLOADS_IMAGE_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE
            }
        ],
        'max_files': 5,
        'key': AttachmentKey.STUDENT_DOCUMENTS
    }


def company_avatar_config():
    return {
        'content_types_configuration': [
            {
                'content_types': settings.USER_UPLOADS_IMAGE_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE
            }
        ],
        'max_files': 1,
        'key': AttachmentKey.COMPANY_AVATAR
    }


def company_documents_config():
    return {
        'content_types_configuration': [
            {
                'content_types': settings.USER_UPLOADS_VIDEO_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_VIDEO_SIZE
            },
            {
                'content_types': settings.USER_UPLOADS_DOCUMENT_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_DOCUMENT_SIZE
            },
            {
                'content_types': settings.USER_UPLOADS_IMAGE_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE
            }
        ],
        'max_files': 5,
        'key': AttachmentKey.COMPANY_DOCUMENTS
    }


upload_configurations = [
    student_avatar_config(),
    student_documents_config(),
    company_avatar_config(),
    company_documents_config()
]