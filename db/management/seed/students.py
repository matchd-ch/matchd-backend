import json
import os

import magic
from PIL import Image as PILImage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from graphql_auth.models import UserStatus

from db.helper.forms import convert_date
from db.models import ProfileType, Student as StudentModel, Image, Attachment, AttachmentKey


class Student:

    users = None

    def run(self):
        self.read_users()
        index = 1
        for user in self.users:
            self.create_student(user, index)
            index += 1

    def read_users(self):
        with open('db/management/seed/students.json') as json_file:
            self.users = json.load(json_file)

    def create_student(self, user_data, index):
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        username = 'student-%s@matchd.lo' % str(index)

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
                type=ProfileType.STUDENT,
                first_name=first_name,
                last_name=last_name
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

        try:
            student = StudentModel.objects.get(user=user)
        except StudentModel.DoesNotExist:
            student = StudentModel.objects.create(user=user)

        student.mobile = user_data.get('mobile')
        student.street = user_data.get('street')
        student.zip = user_data.get('street')
        student.city = user_data.get('city')
        student.date_of_birth = convert_date(user_data.get('date_of_birth'), '%d.%m.%Y')
        student.nickname = user_data.get('nickname')
        student.school_name = user_data.get('school_name')
        student.field_of_study = user_data.get('field_of_study')
        student.graduation = convert_date(user_data.get('graduation'), '%m.%Y')
        student.job_option = user_data.get('job_option')
        student.job_from_date = user_data.get('job_from_date')
        student.job_to_date = user_data.get('job_to_date')
        student.job_position = user_data.get('job_position')
        student.skills.set(user_data.get('skills'))
        student.distinction = user_data.get('distinction')
        student.state = user_data.get('state')
        student.profile_step = user_data.get('profile_step')
        student.soft_skills.set(user_data.get('soft_skills'))
        student.cultural_fits.set(user_data.get('cultural_fits'))
        student.save()

        self.add_profile_image(user, user_data)

        return user

    def add_profile_image(self, user, user_data):
        # check if original folder still exists
        origin_folder = os.path.join(settings.MEDIA_ROOT, 'student', user.username)
        origin_folder_exists = os.path.exists(origin_folder)
        generated_folder = os.path.join(settings.MEDIA_ROOT, 'student', str(user.id))
        generated_folder_exists = os.path.exists(generated_folder)

        # raise exception if the original folder and the generated folder do not exist
        if not origin_folder_exists and not generated_folder_exists:
            print('Missing media_fixtures: ', origin_folder)
            print('Ensure media_fixtures are up to date. Run ./init.sh')
            raise Exception('Missing media fixtures')

        # rename folder if destination does not exist
        if origin_folder_exists and not generated_folder_exists:
            os.rename(origin_folder, generated_folder)
        elif origin_folder_exists and generated_folder_exists:
            print('copy files...')

        avatar = user_data.get('avatar')

        profile_image_path = os.path.join(generated_folder, 'images', avatar)
        if not os.path.exists(profile_image_path):
            print('Missing media_fixtures: ', profile_image_path)
            print('Ensure media_fixtures are up to date. Run ./init.sh')
            raise Exception('Missing media_fixtures')

        relative_image_path = os.path.join('student', str(user.id), 'images', avatar)

        # create image
        try:
            image = Image.objects.get(file=relative_image_path)
        except Image.DoesNotExist:
            image = Image.objects.create(
                file=relative_image_path,
                collection_id=1,
                uploaded_by_user_id=user.id
            )

        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(profile_image_path)
        image.mime_type = mime_type

        with PILImage.open(profile_image_path) as img:
            width, height = img.size

        image.width = width
        image.height = height

        image.save()

        # create attachment
        student_content_type = user.get_profile_content_type()
        student_id = user.get_profile_id()

        image_content_type = ContentType.objects.get(model='image', app_label='db')

        try:
            attachment = Attachment.objects.get(attachment_type=image_content_type, content_type=student_content_type,
                                                object_id=student_id, attachment_id=image.id)
        except Attachment.DoesNotExist:
            attachment = Attachment.objects.create(
                attachment_type=image_content_type, content_type=student_content_type,
                object_id=student_id, attachment_id=image.id
            )

        attachment.key = AttachmentKey.STUDENT_AVATAR
        attachment.save()

