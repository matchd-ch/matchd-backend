import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model

from db.models import Image


class Media:

    def run(self):

        media_path = settings.MEDIA_ROOT
        random_images_path = os.path.join(media_path, 'random')
        admin_user = get_user_model().objects.get(username='admin')
        if not admin_user:
            raise Exception('Admin user not found. Could not seed random images')

        for i in range(1, settings.NUMBER_OF_RANDOM_PROFILE_IMAGES + 1):
            source_path = os.path.join('db', 'seed', 'media', f'r-{i}.png')
            destination_path = os.path.join(random_images_path, f'r-{i}.png')
            os.makedirs(random_images_path, exist_ok=True)
            if not os.path.exists(destination_path):
                shutil.copy(source_path, destination_path)

            image, created = Image.objects.get_or_create(file=os.path.join('random', f'r-{i}.png'))
            image.uploaded_by_user = admin_user
            image.mime_type = 'image/png'
            image.collection_id = 1
            image.save()
