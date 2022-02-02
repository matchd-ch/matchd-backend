import os
import shutil

import magic
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from PIL import Image as PILImage

from db.seed.base import BaseSeed
from db.models import Attachment as AttachmentModel, ProfileState, Image, Video, File, AttachmentKey


# pylint: disable=W0612
# pylint: disable=R0913
# pylint: disable=W0612
class Attachment(BaseSeed):

    company_fixtures = os.path.join(settings.MEDIA_FIXTURE_ROOT, 'company')
    student_fixtures = os.path.join(settings.MEDIA_FIXTURE_ROOT, 'student')

    content_types = {
        'company': ContentType.objects.get(app_label='db', model='company'),
        'student': ContentType.objects.get(app_label='db', model='student'),
        'video': ContentType.objects.get(app_label='db', model='video'),
        'image': ContentType.objects.get(app_label='db', model='image'),
        'file': ContentType.objects.get(app_label='db', model='file'),
        'projectposting': ContentType.objects.get(app_label='db', model='projectposting'),
    }

    def _get_dirs_and_file(self, path):
        parts = path.split('/')
        if len(parts) == 0:
            return [], parts[0]
        file = parts[-1]
        dirs = parts[:-1]
        return dirs, file

    def _dir_for_type(self, model):
        if model == 'image':
            return 'images'
        if model == 'video':
            return 'videos'
        if model == 'file':
            return 'documents'
        return ''

    def _create_image(self, image_path, relative_path, user):
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

    def _create_video(self, relative_path, user):
        video, created = Video.objects.get_or_create(file=relative_path)
        video.uploaded_by_user = user
        video.collection_id = 1

        video.save()
        return video

    def _create_file(self, relative_path, user):
        video, created = File.objects.get_or_create(file=relative_path)
        video.uploaded_by_user = user
        video.collection_id = 1
        video.save()
        return video

    def _create_attachment(self, fixtures, company_or_student_project_posting, data, user,
                           content_type_key):
        media_path = os.path.join(settings.MEDIA_ROOT)
        app_label, model = data.get('type').split('.')
        dirs, file = self._get_dirs_and_file(data.get('file'))
        source_file = os.path.join(fixtures, *dirs, file)
        relative_path = os.path.join(content_type_key, str(company_or_student_project_posting.id),
                                     self._dir_for_type(model))
        relative_file_path = os.path.join(relative_path, file)

        destination_directory = os.path.join(media_path, relative_path)
        os.makedirs(destination_directory, exist_ok=True)
        destination_file = os.path.join(destination_directory, file)

        if not os.path.exists(destination_file):
            shutil.copy(source_file, destination_file)

        attachment_instance = None
        if model == 'image':
            attachment_instance = self._create_image(destination_file, relative_file_path, user)
        elif model == 'video':
            attachment_instance = self._create_video(relative_file_path, user)
        elif model == 'file':
            attachment_instance = self._create_file(relative_file_path, user)

        attachment_key = data.get('key')
        if attachment_key in (AttachmentKey.COMPANY_AVATAR, AttachmentKey.STUDENT_AVATAR):
            existing = AttachmentModel.objects.filter(
                key=attachment_key,
                object_id=company_or_student_project_posting.id,
                content_type=self.content_types[content_type_key])

            for obj in existing:
                if obj.attachment_id == attachment_instance.id:
                    continue
                obj.attachment_object.delete()
                obj.delete()

        AttachmentModel.objects.get_or_create(attachment_type=self.content_types[model],
                                              attachment_id=attachment_instance.id,
                                              content_type=self.content_types[content_type_key],
                                              object_id=company_or_student_project_posting.id,
                                              key=attachment_key)

    def _create_or_update_company(self, data, company, user):
        if company.state == ProfileState.INCOMPLETE:
            return
        attachments = data.get('company').get('attachments')

        if attachments is None:
            attachments = []
            moods = self.rand.moods()
            avatar = self.rand.logo()
            attachments.append({
                "file": f'avatars/{avatar}',
                "key": "company_avatar",
                "type": "db.image",
                "user": user.email
            })
            for mood in moods:
                attachments.append({
                    "file": f'moods/{mood}',
                    "key": "company_documents",
                    "type": "db.image",
                    "user": user.email
                })

        for attachment in attachments:
            user = get_user_model().objects.get(email=attachment.get('user'))
            self._create_attachment(self.company_fixtures, company, attachment, user, 'company')

    def _create_or_update_student(self, data, student):
        if student.state == ProfileState.INCOMPLETE:
            return
        attachments = data.get('student').get('attachments')

        if attachments is None:
            gender = self.rand.gender()
            avatar_fixtures_dir = os.path.join(self.student_fixtures, 'avatars')
            avatar = self.rand.avatar(gender)

            avatar = {
                "file": f"{gender}/{avatar}",
                "key": "student_avatar",
                "type": "db.image",
                "user": student.user.email
            }
            self._create_attachment(avatar_fixtures_dir, student, avatar, student.user, 'student')
            documents_fixtures_dir = os.path.join(self.student_fixtures, 'documents')
            documents = self.rand.documents()
            for document in documents:
                document_data = {
                    "file": f"{document}",
                    "key": "student_documents",
                    "type": "db.file",
                    "user": student.user.email
                }
                self._create_attachment(documents_fixtures_dir, student, document_data,
                                        student.user, 'student')

        for attachment in attachments:
            user = get_user_model().objects.get(email=attachment.get('user'))
            self._create_attachment(self.student_fixtures, student, attachment, user, 'student')

    def _create_or_update_project_posting(self, project_posting):
        content_type = ContentType.objects.get(app_label='db', model='projectposting')
        images = AttachmentModel.objects.filter(key=AttachmentKey.PROJECT_POSTING_IMAGES,
                                                content_type=content_type,
                                                object_id=project_posting.id)

        documents = AttachmentModel.objects.filter(key=AttachmentKey.PROJECT_POSTING_DOCUMENTS,
                                                   content_type=content_type,
                                                   object_id=project_posting.id)

        user = None
        if project_posting.student is not None:
            user = project_posting.student.user
        if project_posting.employee is not None:
            user = project_posting.employee.user

        if len(images) == 0 and project_posting.id % 2 == 0:
            for i in range(1, self.rand.number()):
                data = {
                    'file': f'moods/{self.rand.mood()}',
                    'type': 'db.image',
                    'key': 'project_posting_images',
                }
                self._create_attachment(self.company_fixtures, project_posting, data, user,
                                        'projectposting')
        if len(documents) == 0 and project_posting.id % 2 == 0:
            for i in range(1, 3):
                data = {
                    'file': f'documents/doc-{i}.pdf',
                    'type': 'db.file',
                    'key': 'project_posting_documents',
                }
                self._create_attachment(self.student_fixtures, project_posting, data, user,
                                        'projectposting')

    def create_or_update(self, data, *args, **kwargs):
        project_postings = kwargs.get('project_postings')
        if project_postings is not None:
            for project_posting in project_postings:
                self._create_or_update_project_posting(project_posting)
            return
        if data is None:
            return
        company = kwargs.get('company')
        student = kwargs.get('student')
        if company is not None:
            user = kwargs.get('user')
            if len(data.get('company').keys()) > 1:
                self._create_or_update_company(data, company, user)
        if student is not None:
            self._create_or_update_student(data, student)

    def random(self, *args, **kwargs):
        pass
