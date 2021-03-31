import json
import os
import shutil

import magic
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from graphql_auth.models import UserStatus
from PIL import Image as PILImage

from db.models import Image, Attachment, Video, File


class BaseSeed:

    data = None

    def __init__(self, stdout, file):
        self.stdout = stdout
        self.file = file
        self.data = None
        self.load_data()

    def load_data(self):
        with open('db/management/seed/%s' % self.file) as json_file:
            self.data = json.load(json_file)

    def run(self):
        index = 1
        for user in self.data:
            self.handle_item(user, index)
            index += 1

    def handle_item(self, data, index):
        self.stdout.write('You should customize handle_item in your sub-class')
        pass

    def create_user(self, username, user_type, first_name, last_name, company=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            user = user_model.objects.create(
                username=username,
                email=username,
                is_staff=False,
                is_active=True,
                is_superuser=False,
                type=user_type,
                first_name=first_name,
                last_name=last_name,
                company=company
            )

        user.set_password('asdf1234$')
        user.save()

        try:
            status = UserStatus.objects.get(user=user)
        except UserStatus.DoesNotExist:
            status = UserStatus.objects.create(
                user=user,
                verified=True,
                archived=False
            )

        status.verified = True
        status.save()
        return user

    def prepare_fixtures(self, copy_folder, base_folder, user_folder, user_id):
        # check if original folder still exists
        origin_folder = os.path.join(settings.MEDIA_ROOT, base_folder, user_folder)
        origin_folder_exists = os.path.exists(origin_folder)
        generated_folder = os.path.join(settings.MEDIA_ROOT, base_folder, str(user_id))
        generated_folder_exists = os.path.exists(generated_folder)

        # raise exception if the original folder and the generated folder do not exist
        if not origin_folder_exists and not generated_folder_exists:
            print('Missing media_fixtures: ', origin_folder)
            print('Ensure media_fixtures are up to date. Run ./init.sh')
            raise Exception('Missing media fixtures')

        # delete existing folder
        if generated_folder_exists:
            shutil.rmtree(generated_folder)

        # copy or rename folder
        if copy_folder:
            shutil.copytree(origin_folder, generated_folder)
        else:
            os.rename(origin_folder, generated_folder)

        return generated_folder

    def create_image(self, user, image_path, relative_path):
        if not os.path.exists(image_path):
            print('Missing media_fixtures: ', image_path)
            print('Ensure media_fixtures are up to date. Run ./init.sh')
            raise Exception('Missing media_fixtures')

        # create image
        try:
            image = Image.objects.get(file=relative_path)
        except Image.DoesNotExist:
            image = Image.objects.create(
                file=relative_path,
                collection_id=1,
                uploaded_by_user_id=user.id
            )

        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(image_path)
        image.mime_type = mime_type

        with PILImage.open(image_path) as img:
            width, height = img.size

        image.width = width
        image.height = height

        image.save()
        return image

    def create_attachment(self, student_or_company, image_document_or_video, key):

        owner_content_type = student_or_company.get_profile_content_type()
        owner_id = student_or_company.get_profile_id()

        if isinstance(image_document_or_video, Image):
            attachment_content_type = ContentType.objects.get(model='image', app_label='db')
        elif isinstance(image_document_or_video, Video):
            attachment_content_type = ContentType.objects.get(model='video', app_label='db')
        elif isinstance(image_document_or_video, File):
            attachment_content_type = ContentType.objects.get(model='file', app_label='db')
        else:
            raise Exception('Unknown attachment type')

        try:
            attachment = Attachment.objects.get(attachment_type=attachment_content_type,
                                                content_type=owner_content_type, object_id=owner_id,
                                                attachment_id=image_document_or_video.id)
        except Attachment.DoesNotExist:
            attachment = Attachment.objects.create(
                attachment_type=attachment_content_type, content_type=owner_content_type,
                object_id=owner_id, attachment_id=image_document_or_video.id
            )

        attachment.key = key
        attachment.save()
