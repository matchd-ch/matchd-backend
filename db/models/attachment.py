from django.apps import apps
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

    @classmethod
    def valid_student_keys(cls):
        return [
            cls.STUDENT_AVATAR,
            cls.STUDENT_DOCUMENTS
        ]

    @classmethod
    def valid_company_keys(cls):
        return [
            cls.COMPANY_AVATAR,
            cls.COMPANY_DOCUMENTS
        ]


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
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE,
                'model': settings.WAGTAILIMAGES_IMAGE_MODEL
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
                'max_size': settings.USER_UPLOADS_MAX_VIDEO_SIZE,
                'model': settings.WAGTAILMEDIA_MEDIA_MODEL
            },
            {
                'content_types': settings.USER_UPLOADS_DOCUMENT_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_DOCUMENT_SIZE,
                'model': settings.WAGTAILDOCS_DOCUMENT_MODEL
            },
            {
                'content_types': settings.USER_UPLOADS_IMAGE_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE,
                'model': settings.WAGTAILIMAGES_IMAGE_MODEL
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
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE,
                'model': settings.WAGTAILIMAGES_IMAGE_MODEL
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
                'max_size': settings.USER_UPLOADS_MAX_VIDEO_SIZE,
                'model': settings.WAGTAILMEDIA_MEDIA_MODEL
            },
            {
                'content_types': settings.USER_UPLOADS_DOCUMENT_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_DOCUMENT_SIZE,
                'model': settings.WAGTAILDOCS_DOCUMENT_MODEL
            },
            {
                'content_types': settings.USER_UPLOADS_IMAGE_TYPES,
                'max_size': settings.USER_UPLOADS_MAX_IMAGE_SIZE,
                'model': settings.WAGTAILIMAGES_IMAGE_MODEL
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


def get_config_for_key(key):
    config = None
    for key_config in upload_configurations:
        if key_config.get('key', None) == key:
            config = key_config
            break
    return config


def get_attachment_validator_map_for_key(key):
    config = get_config_for_key(key)
    return [
        (apps.get_model(content_type.get('model')), content_type.get('content_types'), content_type.get('max_size'))
        for content_type in config.get('content_types_configuration', [])
    ]


def get_max_files_for_key(key):
    config = get_config_for_key(key)
    return config.get('max_files')
