import json
import os
import random
import shutil

import magic
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from graphql_auth.models import UserStatus
from PIL import Image as PILImage

from db.models import Employee, Student, Hobby, OnlineProject, UserLanguageRelation, CulturalFit, Skill, SoftSkill, \
    Branch, JobType, ProfileState, Language, LanguageLevel, Company, Image, Video, Attachment, AttachmentKey


class Command(BaseCommand):
    help = 'Generates test data'
    data = []

    random_hobbies = [
        'Gamen', 'Fussball', 'Programmieren', 'Kochen', 'Jodeln', 'Wandern', 'Handball', 'Lego', 'Gitarre', 'Flöte',
        'mit dem Hund spazieren', 'Kollegen treffen', 'Ausgang', 'Bowling', 'Malen', 'Zeichnen'
    ]

    content_types = {
        'company': ContentType.objects.get(app_label='db', model='company'),
        'student': ContentType.objects.get(app_label='db', model='student'),
        'video': ContentType.objects.get(app_label='db', model='video'),
        'image': ContentType.objects.get(app_label='db', model='image'),
        'file': ContentType.objects.get(app_label='db', model='file')
    }

    random_cultural_fits = []
    random_skills = []
    random_soft_skills = []
    random_branches = []
    random_job_types = []
    random_languages = []
    random_language_levels = []

    def load_data(self):
        with open('db/management/seed/fixtures.json') as json_file:
            self.data = json.load(json_file)

        self.random_cultural_fits = list(CulturalFit.objects.all().values_list('id', flat=True))
        self.random_skills = list(Skill.objects.all().values_list('id', flat=True))
        self.random_soft_skills = list(SoftSkill.objects.all().values_list('id', flat=True))
        self.random_branches = list(Branch.objects.all().values_list('id', flat=True))
        self.random_job_types = list(JobType.objects.all().values_list('id', flat=True))
        self.random_languages = list(Language.objects.all().values_list('id', flat=True))
        self.random_language_levels = list(LanguageLevel.objects.all().values_list('id', flat=True))

    def random_items(self, items, count):
        random.shuffle(items)
        if count == 1:
            return items[0]
        return items[:count]

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):
        self.load_data()
        self.stdout.write('Adding test data...')

        # create users first
        for user_data in self.data:
            user = self.create_user(user_data)
            self.create_employee(user, user_data.get('employee'))
            student = self.create_student(user, user_data.get('student'))
            company = self.create_company(user, user_data.get('company'))

            if company is not None:
                self.create_attachments_for_company(company, user_data)

            if student is not None:
                self.create_attachments_for_student(student, user_data)

        self.stdout.write(self.style.SUCCESS('Adding test data completed'))

    def create_user(self, data):
        email = data.get('email')
        user, created = get_user_model().objects.get_or_create(email=email)
        user.username = email
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.type = data.get('type')
        user.set_password('asdf1234$')
        user.save()

        user_status, created = UserStatus.objects.get_or_create(user=user)
        user_status.verified = data.get('verified')
        user_status.save()
        return user

    def create_company(self, user, data):
        if data is None:
            return None
        company, created = Company.objects.get_or_create(slug=data.get('slug'))
        user.company = company
        user.save()

        if len(data.keys()) == 1:
            return company

        company.state = data.get('state')
        is_complete = company.state != ProfileState.INCOMPLETE

        # benefits
        company.branches.set(data.get('branches'))
        branches = data.get('branches')
        if len(branches) == 0 and is_complete and len(user.company.branches.all()) == 0:
            company.branches.set(self.random_items(self.random_branches, 6))
        else:
            company.cultural_fits.set(branches)
        company.city = data.get('city')
        cultural_fits = data.get('cultural_fits')
        if len(cultural_fits) == 0 and is_complete and len(company.cultural_fits.all()) == 0:
            company.cultural_fits.set(self.random_items(self.random_cultural_fits, 6))
        else:
            company.cultural_fits.set(cultural_fits)
        company.description = data.get('description')
        company.link_education = data.get('link_education', None)
        company.link_projects = data.get('link_projects', None)
        company.link_thesis = data.get('link_thesis', None)
        company.member_it_st_gallen = data.get('member_it_st_gallen', 0)
        company.name = data.get('name')
        company.phone = data.get('phone')
        company.profile_step = data.get('profile_step')
        company.services = data.get('services', '')
        soft_skills = data.get('soft_skills')
        if len(soft_skills) == 0 and is_complete and len(company.soft_skills.all()) == 0:
            company.soft_skills.set(self.random_items(self.random_soft_skills, 4))
        else:
            company.soft_skills.set(soft_skills)

        company.street = data.get('street')
        company.top_level_organisation_description = data.get('top_level_organisation_description', '')
        company.top_level_organisation_website = data.get('top_level_organisation_website', '')
        company.type = data.get('type')
        company.uid = data.get('uid', '')
        company.website = data.get('website')
        company.zip = data.get('zip')

        company.save()
        return company

    def create_employee(self, user, data):
        if data is None:
            return

        employee, created = Employee.objects.get_or_create(user=user)
        employee.role = data.get('role')
        employee.save()

    def create_student(self, user, data):
        if data is None:
            return None
        student, created = Student.objects.get_or_create(user=user)
        is_complete = user.student.state != ProfileState.INCOMPLETE

        branch = data.get('branch')
        if branch is None and is_complete:
            student.branch_id = self.random_items(self.random_branches, 1)
        else:
            student.branch_id = branch
        student.city = data.get('city')
        cultural_fits = data.get('cultural_fits')
        if len(cultural_fits) == 0 and is_complete and len(user.student.cultural_fits.all()) == 0:
            student.cultural_fits.set(self.random_items(self.random_cultural_fits, 6))
        else:
            student.cultural_fits.set(cultural_fits)
        student.date_of_birth = data.get('date_of_birth')
        student.distinction = data.get('distinction')
        student.field_of_study = data.get('field_of_study')
        student.graduation = data.get('graduation')
        hobbies = data.get('hobbies')
        if len(data.get('hobbies')) == 0 and is_complete and len(user.student.hobbies.all()) == 0:
            for hobby in self.random_items(self.random_hobbies, 3):
                Hobby.objects.create(student=student, name=hobby)
        else:
            for hobby in hobbies:
                Hobby.objects.get_or_create(student=student, name=hobby)

        student.job_from_date = data.get('job_from_date')
        student.job_to_date = data.get('job_to_date')
        job_type = data.get('job_type')
        if job_type is None and is_complete:
            student.job_type_id = self.random_items(self.random_job_types, 1)
        else:
            student.job_type_id = job_type

        languages = data.get('languages')
        if len(languages) == 0 and is_complete and len(user.student.languages.all()) == 0:
            random_languages = self.random_items(self.random_languages, 3)
            random_language_levels = self.random_items(self.random_language_levels, 3)
            index = 0
            for language in random_languages:
                UserLanguageRelation.objects.create(student=student, language_id=language,
                                                    language_level_id=random_language_levels[index])
                index += 1
        else:
            for language in languages:
                UserLanguageRelation.objects.get_or_create(student=student, language_id=language.get('language'),
                                                           language_level_id=language.get('language_level'))
        student.mobile = data.get('mobile')
        student.nickname = data.get('nickname')
        online_projects = data.get('online_projects')
        if len(online_projects) == 0 and is_complete and len(user.student.online_projects.all()) == 0:
            OnlineProject.objects.create(student=student, url='http://www.project.lo')
            OnlineProject.objects.create(student=student, url='http://www.project2.lo')
        else:
            for online_project in online_projects:
                OnlineProject.objects.get_or_create(student=student, url=online_project)
        student.profile_step = data.get('profile_step')
        student.school_name = data.get('school_name')

        skills = data.get('skills')
        if len(skills) == 0 and is_complete and len(user.student.skills.all()) == 0:
            student.skills.set(self.random_items(self.random_skills, 4))
        else:
            student.skills.set(skills)

        soft_skills = data.get('soft_skills')
        if len(soft_skills) == 0 and is_complete and len(user.student.soft_skills.all()) == 0:
            student.soft_skills.set(self.random_items(self.random_soft_skills, 4))
        else:
            student.soft_skills.set(soft_skills)

        student.state = data.get('state')
        student.zip = data.get('street')
        student.save()
        return student

    def create_attachments_for_student(self, student, user_data):
        attachments = user_data.get('student').get('attachments')
        if attachments is None:
            return
        fixtures_path = os.path.join(settings.MEDIA_ROOT, 'student_fixtures')

        for attachment in attachments:
            user = student.user
            self.create_attachment(fixtures_path, student, attachment, user, 'student')

    def create_attachments_for_company(self, company, user_data):
        attachments = user_data.get('company').get('attachments')
        if attachments is None:
            return
        fixtures_path = os.path.join(settings.MEDIA_ROOT, 'company_fixtures')

        for attachment in attachments:
            # print(attachment)
            user = get_user_model().objects.get(email=attachment.get('user'))
            self.create_attachment(fixtures_path, company, attachment, user, 'company')

    def create_attachment(self, fixtures_path, company_or_student, attachment_data, user, content_type_key):
        media_path = os.path.join(settings.MEDIA_ROOT)

        app_label, model = attachment_data.get('type').split('.')
        file_path = os.path.join(fixtures_path, attachment_data.get('file'))
        relative_path = os.path.join('company', str(company_or_student.id), 'images' if model == 'image' else 'video')
        relative_file_path = os.path.join('company', str(company_or_student.id), 'images' if model == 'image' else 'video',
                                          attachment_data.get('file'))

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

        Attachment.objects.get_or_create(
            attachment_type=self.content_types[model], attachment_id=attachment_instance.id,
            content_type=self.content_types[content_type_key], object_id=company_or_student.id,
            key=attachment_data.get('key'))

    def create_image(self, image_path, relative_path, user):
        image, created = Image.objects.get_or_create(file=relative_path)
        image.uploaded_by_user = user
        image.collection_id = 1

        if image.mime_type is None or image.mime_type == '':
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(image_path)
            image.mime_type = mime_type

        if image.width is None or image.width == '':
            with PILImage.open(image_path) as img:
                width, height = img.size

            image.width = width
            image.height = height

        image.save()
        return image

    def create_video(self, relative_path, user):
        video, created = Video.objects.get_or_create(file=relative_path)
        video.uploaded_by_user = user
        video.collection_id = 1

        video.save()
        return video
