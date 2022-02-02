import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from db.models import Image, Attachment, AttachmentKey


class Media:

    def run(self):

        media_path = settings.MEDIA_ROOT
        random_images_path = os.path.join(media_path, 'random')
        admin_user = get_user_model().objects.get(username='admin')
        if not admin_user:
            raise Exception('Admin user not found. Could not seed random images')

        image_content_type = ContentType.objects.get(app_label='db', model='image')
        user_content_type = ContentType.objects.get(app_label='db', model='user')

        for i in range(1, settings.NUMBER_OF_STUDENT_AVATAR_FALLBACK_IMAGES + 1):
            image_name = f's-{i}.png'
            source_path = os.path.join('db', 'seed', 'media', image_name)
            destination_path = os.path.join(random_images_path, image_name)
            os.makedirs(random_images_path, exist_ok=True)
            if not os.path.exists(destination_path):
                shutil.copy(source_path, destination_path)

            # pylint: disable=W0612
            image, created = Image.objects.get_or_create(file=os.path.join('random', image_name))
            image.uploaded_by_user = admin_user
            image.mime_type = 'image/png'
            image.collection_id = 1
            image.save()

            Attachment.objects.get_or_create(attachment_id=image.id,
                                             attachment_type_id=image_content_type.id,
                                             content_type_id=user_content_type.id,
                                             object_id=admin_user.id,
                                             key=AttachmentKey.STUDENT_AVATAR_FALLBACK)

        for i in range(1, settings.NUMBER_OF_COMPANY_AVATAR_FALLBACK_IMAGES + 1):
            image_name = f'c-{i}.png'
            source_path = os.path.join('db', 'seed', 'media', image_name)
            destination_path = os.path.join(random_images_path, image_name)
            os.makedirs(random_images_path, exist_ok=True)
            if not os.path.exists(destination_path):
                shutil.copy(source_path, destination_path)

            image, created = Image.objects.get_or_create(file=os.path.join('random', image_name))
            image.uploaded_by_user = admin_user
            image.mime_type = 'image/png'
            image.collection_id = 1
            image.save()

            image_content_type = ContentType.objects.get(app_label='db', model='image')
            user_content_type = ContentType.objects.get(app_label='db', model='user')

            Attachment.objects.get_or_create(attachment_id=image.id,
                                             attachment_type_id=image_content_type.id,
                                             content_type_id=user_content_type.id,
                                             object_id=admin_user.id,
                                             key=AttachmentKey.COMPANY_AVATAR_FALLBACK)

        for i in range(1, settings.NUMBER_OF_PROJECT_POSTING_FALLBACK_IMAGES + 1):
            image_name = f'p-{i}.png'
            source_path = os.path.join('db', 'seed', 'media', image_name)
            destination_path = os.path.join(random_images_path, image_name)
            os.makedirs(random_images_path, exist_ok=True)
            if not os.path.exists(destination_path):
                shutil.copy(source_path, destination_path)

            image, created = Image.objects.get_or_create(file=os.path.join('random', image_name))
            image.uploaded_by_user = admin_user
            image.mime_type = 'image/png'
            image.collection_id = 1
            image.save()

            image_content_type = ContentType.objects.get(app_label='db', model='image')
            user_content_type = ContentType.objects.get(app_label='db', model='user')

            Attachment.objects.get_or_create(attachment_id=image.id,
                                             attachment_type_id=image_content_type.id,
                                             content_type_id=user_content_type.id,
                                             object_id=admin_user.id,
                                             key=AttachmentKey.PROJECT_POSTING_FALLBACK)
