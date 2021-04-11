import os
import shutil

from django.conf import settings
from django.utils.text import slugify

from .seed import Command as SeedCommand


# pylint: disable=W0612
# pylint: disable=R0902
# pylint: disable=R0912
# pylint: disable=R0913
# pylint: disable=R0915
from ...models import Attachment


class Command(SeedCommand):
    help = 'Generates a lot of dummy students'

    def add_arguments(self, parser):
        parser.add_argument('num', type=int, help='Indicates the number of students to be created', default=0)

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):
        number_of_students = options.get('num')
        self.stdout.write(f'Adding {number_of_students} dummy student(s)...')
        self.load_data()
        data = []
        for i in range(0, number_of_students):
            email = f"dummy-{str(i)}@matchd.lo"
            languages = []
            random_languages = self.random_items(self.random_languages, 3)
            random_language_levels = self.random_items(self.random_language_levels, 3)
            for j in range(0, 3):
                obj = {
                    "language": random_languages[j],
                    "language_level": random_language_levels[j]
                }
                languages.append(obj)

            name, gender = self.random_name()
            nickname = f'{slugify(name)}-{str(i)}'
            first_name, last_name = name.split(' ')

            street, zip_value, city = self.random_items(self.random_address, 1)

            avatar = self.random_items(self.random_male_avatars, 1)
            if gender == 'female':
                avatar = self.random_items(self.random_female_avatars, 1)

            dummy = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "student": {
                    "attachments": [
                        {
                            "file": avatar,
                            "key": "student_avatar",
                            "type": "db.image",
                            "user": email
                        }
                    ],
                    "branch": self.random_items(self.random_branches, 1),
                    "city": city,
                    "cultural_fits": self.random_items(self.random_cultural_fits, 6),
                    "date_of_birth": "2002-04-05",
                    "distinction": "Distinction",
                    "field_of_study": "Applikationsentwicklung",
                    "graduation": "2022-08-01",
                    "hobbies": self.random_items(self.random_hobbies, 2),
                    "job_from_date": self.random_start_date(),
                    "job_to_date": self.random_end_date(),
                    "job_type": self.random_items(self.random_job_types, 1),
                    "languages": languages,
                    "mobile": "+791234567",
                    "nickname": nickname,
                    "slug": slugify(nickname),
                    "online_projects": [
                        "http://www.project.lo",
                        "http://www.project2.lo"
                    ],
                    "profile_step": 7,
                    "school_name": "FH Winterthur",
                    "skills": self.random_items(self.random_skills, 4),
                    "soft_skills": self.random_items(self.random_soft_skills, 6),
                    "state": "public",
                    "street": street,
                    "zip": zip_value
                },
                "type": "student",
                "verified": 1
            }

            data.append(dummy)

        for user_data in data:
            self.stdout.write('.', ending='')
            user = self.create_user(user_data)
            student = self.create_student(user, user_data.get('student'))
            if student is not None:
                self.create_attachments_for_student(student, user_data)
        self.stdout.write('', ending='\n')
        self.stdout.write(self.style.SUCCESS('Adding test data completed'))

    def create_attachment(self, fixtures_path, company_or_student, attachment_data, user, content_type_key):
        media_path = os.path.join(settings.MEDIA_ROOT)

        app_label, model = attachment_data.get('type').split('.')
        file_path = os.path.join(fixtures_path, attachment_data.get('file'))
        relative_path = os.path.join(content_type_key, str(company_or_student.id),
                                     'images' if model == 'image' else 'video')
        relative_file_path = os.path.join(content_type_key, str(company_or_student.id),
                                          'images' if model == 'image' else 'video', attachment_data.get('file'))

        destination_path = os.path.join(media_path, relative_path)
        os.makedirs(destination_path, exist_ok=True)
        destination_path = os.path.join(destination_path, attachment_data.get('file'))

        if not os.path.exists(destination_path):
            shutil.copy(file_path, destination_path)

        attachment_instance = None
        if model == 'image':
            attachment_instance = self.create_image(destination_path, relative_file_path, user)
        elif model == 'video':
            attachment_instance = self.create_video(relative_file_path, user)

        try:
            data = Attachment.objects.get(
                attachment_type=self.content_types[model],
                content_type=self.content_types[content_type_key], object_id=company_or_student.id,
                key=attachment_data.get('key'))
            data.attachment_id = attachment_instance.id
            data.save()
        except Attachment.DoesNotExist:
            Attachment.objects.create(
                attachment_type=self.content_types[model], attachment_id=attachment_instance.id,
                content_type=self.content_types[content_type_key], object_id=company_or_student.id,
                key=attachment_data.get('key'))
