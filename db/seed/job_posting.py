from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from db.models import ProfileState, JobPosting as JobPostingModel, DateMode, JobPostingState, Employee, \
    JobPostingLanguageRelation, JobType, ProfileType
from db.seed.base import BaseSeed


# pylint: disable=W0612
# pylint: disable=R0912
# pylint: disable=R0915
class JobPosting(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):
        if data is None:
            return
        if len(data.get('company').keys()) == 1:
            return
        company = kwargs.get('company')
        if company.state == ProfileState.INCOMPLETE:
            return
        if company.type != ProfileType.COMPANY:
            return

        user = kwargs.get('user')

        job_postings = data.get('company').get('job_postings')
        if job_postings is None or len(job_postings) == 0:
            for i in range(0, self.rand.number()):
                job_type = self.rand.job_type()
                job_from_date = self.rand.job_from_date()
                job_to_date = None
                job_type_object = JobType.objects.get(pk=job_type)
                if job_type_object.mode == DateMode.DATE_RANGE:
                    job_to_date = self.rand.job_to_date(job_from_date)

                workload_total = self.rand.workload()

                job_posting = JobPostingModel(title=self.rand.title(),
                                              description=self.rand.description(),
                                              job_type_id=job_type,
                                              workload_from=workload_total,
                                              workload_to=workload_total,
                                              company=company,
                                              job_from_date=job_from_date,
                                              job_to_date=job_to_date,
                                              url='https://www.job.lo',
                                              form_step=4,
                                              state=self.rand.job_posting_state(),
                                              employee=Employee.objects.get(user=user))
                job_posting.save()
                if job_posting.state == JobPostingState.PUBLIC:
                    job_posting.date_published = job_posting.date_created
                job_posting.slug = f'{slugify(job_posting.title)}-{str(job_posting.id)}'
                job_posting.save()
                job_posting.job_requirements.set(self.rand.requirements())
                job_posting.skills.set(self.rand.skills())
                job_posting.branches.set(self.rand.branches())
                languages = self.rand.languages_shortlist()
                for language in languages:
                    JobPostingLanguageRelation.objects.create(
                        job_posting=job_posting,
                        language_id=language.get('language'),
                        language_level_id=language.get('language_level'))
        else:
            for obj in job_postings:
                try:
                    job_posting = JobPostingModel.objects.get(slug=obj.get('slug'))
                except JobPostingModel.DoesNotExist:
                    job_posting = JobPostingModel(job_type_id=obj.get('job_type'), company=company)
                job_title = obj.get('title', None)
                if job_title is None:
                    job_title = self.rand.title()
                job_posting.title = job_title
                job_posting.description = obj.get('description')
                workload_from = obj.get('workload_from')
                if workload_from is None or workload_from == '':
                    workload_from = self.rand.workload()
                date_created = obj.get('date_created')
                date_created = datetime.strptime(
                    date_created,
                    '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                date_published = obj.get('date_published')
                if date_published is not None:
                    date_published = datetime.strptime(
                        date_published,
                        '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                if job_posting.state == JobPostingState.PUBLIC and job_posting.date_created is None:
                    job_posting.date_published = job_posting.date_created
                job_posting.date_created = date_created
                job_posting.date_published = date_published
                job_posting.workload_from = workload_from
                job_posting.workload_to = workload_from
                job_posting.job_from_date = obj.get('job_from_date')
                job_posting.job_to_date = obj.get('job_to_date')
                job_posting.url = obj.get('url')
                job_posting.form_step = obj.get('form_step')
                job_posting.state = obj.get('state')
                job_posting.employee = get_user_model().objects.get(
                    email=obj.get('employee')).employee
                job_posting.save()
                slug = obj.get('slug')
                if slug is None or slug == '':
                    slug = f'{slugify(job_posting.title)}-{str(job_posting.id)}'
                job_posting.slug = slug
                job_posting.save()
                job_posting.skills.set(obj.get('skills'))
                job_posting.branches.set(obj.get('branches'))
                job_posting.job_requirements.set(obj.get('job_requirements'))

                languages = obj.get('languages')
                for language in languages:
                    try:
                        rel = JobPostingLanguageRelation.objects.get(
                            job_posting=job_posting, language_id=language.get('language'))
                        rel.language_level_id = language.get('language_level')
                        rel.save()
                    except JobPostingLanguageRelation.DoesNotExist:
                        JobPostingLanguageRelation.objects.create(
                            job_posting=job_posting,
                            language_id=language.get('language'),
                            language_level_id=language.get('language_level'))

    def random(self, *args, **kwargs):
        pass
