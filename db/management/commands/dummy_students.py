import os
import shutil

import names
from django.conf import settings
from django.utils.text import slugify

from .seed import Command as SeedCommand


# pylint: disable=W0612
# pylint: disable=R0902
# pylint: disable=R0912
# pylint: disable=R0913
# pylint: disable=R0915
from ...models import CulturalFit, Skill, SoftSkill, Branch, JobType, Language, LanguageLevel, Attachment


class Command(SeedCommand):
    help = 'Generates a lot of dummy students'

    random_gender = []

    def add_arguments(self, parser):
        parser.add_argument('num', type=int, help='Indicates the number of students to be created', default=0)

    def random_start_date(self):
        months = ['08', '09', '10', '11', '12', '01']
        month = self.random_items(months, 1)
        return f'2021-{month}-01'

    def random_end_date(self):
        months = ['02', '03', '04', '05', '06', '07']
        month = self.random_items(months, 1)
        return f'2022-{month}-01'

    def load_data(self):
        self.load_address_list()
        self.random_cultural_fits = list(CulturalFit.objects.all().values_list('id', flat=True))
        self.random_skills = list(Skill.objects.all().values_list('id', flat=True))
        self.random_soft_skills = list(SoftSkill.objects.all().values_list('id', flat=True))
        self.random_branches = list(Branch.objects.all().values_list('id', flat=True))
        self.random_job_types = list(JobType.objects.all().values_list('id', flat=True))
        self.random_languages = list(Language.objects.all().values_list('id', flat=True))
        self.random_language_levels = list(LanguageLevel.objects.all().values_list('id', flat=True))
        self.random_gender = ['male', 'female']

    def random_name(self):
        gender = self.random_items(self.random_gender, 1)
        name = names.get_full_name(gender=gender)
        return name

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

            name = self.random_name()
            nickname = f'{slugify(name)}-{str(i)}'
            first_name, last_name = name.split(' ')

            street, zip_value, city = self.random_items(self.random_address, 1)

            dummy = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "student": {
                    "attachments": [
                        {
                            "file": "dummy.png",
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
        relative_file_path = attachment_data.get('file')
        destination_path = os.path.join(media_path, attachment_data.get('file'))

        if not os.path.exists(destination_path):
            shutil.copy(file_path, destination_path)

        attachment_instance = None
        if model == 'image':
            attachment_instance = self.create_image(destination_path, relative_file_path, user)
        elif model == 'video':
            attachment_instance = self.create_video(relative_file_path, user)

        Attachment.objects.get_or_create(
            attachment_type=self.content_types[model], attachment_id=attachment_instance.id,
            content_type=self.content_types[content_type_key], object_id=company_or_student.id,
            key=attachment_data.get('key'))
