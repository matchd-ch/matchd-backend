import os
import shutil
import json

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from django.utils.text import slugify

from db.models import Attachment, ProfileType


class Command(BaseCommand):
    help = 'Dumps test data'

    def get_attachments_for_company(self, company):
        content_type = ContentType.objects.get(app_label='db', model='company')
        return self.get_attachments(content_type, company.id, company.slug, 'company_fixtures')

    def get_attachments_for_student(self, student):
        content_type = ContentType.objects.get(app_label='db', model='student')
        return self.get_attachments(content_type, student.id,
                                    slugify(f'{student.user.first_name} {student.user.last_name}'), 'student_fixtures')

    def get_attachments(self, content_type, object_id, slug, directory):
        fixtures_path = os.path.join(settings.MEDIA_ROOT, directory)
        media_path = os.path.join(settings.MEDIA_ROOT)
        attachments = Attachment.objects.filter(content_type_id=content_type.id, object_id=object_id)
        attachment_objs = []

        for attachment in attachments:
            file_path = str(attachment.attachment_object.file)
            source_path = os.path.join(media_path, file_path)
            file_name = file_path.split('/')[-1]
            if slug not in file_name:
                file_name = f'{slug}_{file_name}'
            destination_path = os.path.join(fixtures_path, file_name)
            if not os.path.exists(destination_path):
                shutil.copy(source_path, destination_path)
            attachment_obj = {
                'type': f'{attachment.attachment_type.app_label}.{attachment.attachment_type.model}',
                'file': file_name,
                'user': attachment.attachment_object.uploaded_by_user.email,
                'key': attachment.key
            }
            attachment_objs.append(attachment_obj)
        return attachment_objs

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):
        self.stdout.write('Dumping test data...')

        users = get_user_model().objects.select_related('student').all().exclude(username='admin')
        user_dump = []
        dumped_companies = []

        for user in users:
            user_obj = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'type': user.type,
                'verified': user.status.verified
            }

            if user.type == ProfileType.COMPANY:
                user_obj['employee'] = {
                    'role': user.employee.role
                }

            company = user.company
            if company is not None:
                company_obj = {
                    'slug': company.slug
                }
                if company.slug not in dumped_companies:
                    company_obj.update({
                        'uid': company.uid,
                        'name': company.name,
                        'zip': company.zip,
                        'city': company.city,
                        'description': company.description,
                        'member_it_st_gallen': company.member_it_st_gallen,
                        'phone': company.phone,
                        'services': company.services,
                        'street': company.street,
                        'website': company.website,
                        'profile_step': company.profile_step,
                        'state': company.state,
                        'top_level_organisation_website': company.top_level_organisation_website,
                        'top_level_organisation_description': company.top_level_organisation_description,
                        'type': company.type,
                        'link_education': company.link_education,
                        'link_projects': company.link_projects,
                        'link_thesis': company.link_thesis,
                        'benefits': [obj.id for obj in company.benefits.all()],
                        'branches': [obj.id for obj in company.branches.all()],
                        'cultural_fits': [obj.id for obj in company.cultural_fits.all()],
                        'soft_skills': [obj.id for obj in company.soft_skills.all()],
                        'attachments': self.get_attachments_for_company(company)
                    })
                    dumped_companies.append(company.slug)
                user_obj['company'] = company_obj

            student = getattr(user, 'student', None)
            if student is not None:
                student_obj = {
                    'mobile': student.mobile,
                    'city': student.city,
                    'street': student.street,
                    'zip': student.zip,
                    'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d')
                    if student.date_of_birth is not None else None,
                    'nickname': student.nickname,
                    'field_of_study': student.field_of_study,
                    'graduation': student.graduation.strftime('%Y-%m-%d') if student.graduation is not None else None,
                    'school_name': student.school_name,
                    'job_from_date': student.job_from_date.strftime('%Y-%m-%d')
                    if student.job_from_date is not None else None,
                    'job_to_date': student.job_to_date.strftime('%Y-%m-%d')
                    if student.job_to_date is not None else None,
                    'job_type': student.job_type.id if student.job_type is not None else None,
                    'distinction': student.distinction,
                    'profile_step': student.profile_step,
                    'state': student.state,
                    'branch': student.branch.id if student.branch is not None else None,
                    'cultural_fits': [obj.id for obj in student.cultural_fits.all()],
                    'soft_skills': [obj.id for obj in student.soft_skills.all()],
                    'skills': [obj.id for obj in student.skills.all()],
                    'hobbies': [obj.name for obj in student.hobbies.all()],
                    'online_projects': [obj.url for obj in student.online_projects.all()],
                    'languages': [
                        {'language': obj.language.id, 'language_level': obj.language_level.id}
                        for obj in student.languages.all()
                    ],
                    'attachments': self.get_attachments_for_student(student)
                }
                user_obj['student'] = student_obj

            user_dump.append(user_obj)

        json_string = json.dumps(user_dump, indent=4, sort_keys=True)

        with open('db/management/seed/fixtures.json', 'w') as json_file:
            json_file.write(json_string)

        self.stdout.write(self.style.SUCCESS('Dumping test data completed'))
