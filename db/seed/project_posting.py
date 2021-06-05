from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from db.models import ProfileState, ProjectPosting as ProjectPostingModel, ProjectPostingState
from db.seed.base import BaseSeed


# pylint: disable=W0612
# pylint: disable=R0912
# pylint: disable=R0915
class ProjectPosting(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):
        if data is None:
            return

        if data.get('company') is not None and len(data.get('company').keys()) == 1:
            return

        company = kwargs.get('company')
        project_postings = None
        if company is not None:
            if company.state == ProfileState.INCOMPLETE:
                return
            project_postings = data.get('company').get('project_postings')
        student = kwargs.get('student')
        if student is not None:
            if student.state == ProfileState.INCOMPLETE:
                return
            project_postings = data.get('student').get('project_postings')

        employee = kwargs.get('employee')
        student = kwargs.get('student')
        company = kwargs.get('company')

        if project_postings is None or len(project_postings) == 0:
            for i in range(0, self.rand.number()):

                project_posting = ProjectPostingModel(
                    title=self.rand.project_title(),
                    description=self.rand.description(),
                    additional_information=self.rand.description(),
                    project_type_id=self.rand.project_type(),
                    topic_id=self.rand.topic(),
                    project_from_date=self.rand.project_from_date(),
                    website='https://www.project.lo',
                    form_step=3,
                    state=self.rand.project_posting_state(),
                    employee=employee,
                    company=company,
                    student=student
                )
                project_posting.save()
                if project_posting.state == ProjectPostingState.PUBLIC:
                    project_posting.date_published = project_posting.date_created
                project_posting.slug = f'{slugify(project_posting.title)}-{str(project_posting.id)}'
                project_posting.save()
                project_posting.keywords.set(self.rand.keywords())
        else:
            for obj in project_postings:
                try:
                    project_posting = ProjectPostingModel.objects.get(
                        slug=obj.get('slug'))
                except ProjectPostingModel.DoesNotExist:
                    project_posting = ProjectPostingModel(
                        project_type_id=obj.get('project_type'),
                        topic_id=obj.get('topic'),
                        company=company, employee=employee, student=student)
                project_title = obj.get('title', None)
                if project_title is None:
                    project_title = self.rand.title()
                project_posting.title = project_title
                project_posting.description = obj.get('description')
                project_posting.additional_information = obj.get('additional_information')
                project_posting.website = obj.get('website')
                date_created = obj.get('date_created')
                date_created = datetime.strptime(date_created, '%Y-%m-%d %H:%M:%S').replace(
                    tzinfo=pytz.timezone(settings.TIME_ZONE))
                date_published = obj.get('date_published')
                if date_published is not None:
                    date_published = datetime.strptime(date_published, '%Y-%m-%d %H:%M:%S').replace(
                        tzinfo=pytz.timezone(settings.TIME_ZONE))
                project_posting.date_created = date_created
                project_posting.date_published = date_published
                project_posting.project_from_date = obj.get('project_from_date')
                project_posting.form_step = obj.get('form_step')
                project_posting.state = obj.get('state')
                employee = None
                if obj.get('employee') is not None:
                    employee = get_user_model().objects.get(email=obj.get('employee')).employee
                project_posting.employee = employee
                project_posting.save()
                slug = obj.get('slug')
                if slug is None or slug == '':
                    slug = f'{slugify(project_posting.title)}-{str(project_posting.id)}'
                project_posting.slug = slug
                project_posting.save()
                project_posting.keywords.set(obj.get('keywords'))

    def random(self, *args, **kwargs):
        pass
