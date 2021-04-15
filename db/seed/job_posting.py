from django.contrib.auth import get_user_model
from django.utils.text import slugify

from db.models import ProfileState, JobPosting as JobPostingModel, DateMode, JobPostingState, Employee, \
    JobPostingLanguageRelation, JobType, ProfileType
from db.seed.base import BaseSeed


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

                job_posting = JobPostingModel(
                    title=self.rand.title(),
                    description=self.rand.description(),
                    job_type_id=job_type,
                    branch_id=self.rand.branch(),
                    workload=self.rand.workload(),
                    company=company,
                    job_from_date=job_from_date,
                    job_to_date=job_to_date,
                    url='https://www.job.lo',
                    form_step=4,
                    state=JobPostingState.PUBLIC,
                    employee=Employee.objects.get(user=user)
                )
                job_posting.save()
                job_posting.slug = f'{slugify(job_posting.title)}-{str(job_posting.id)}'
                job_posting.save()
                job_posting.job_requirements.set(self.rand.requirements())
                job_posting.skills.set(self.rand.skills())
                languages = self.rand.languages()
                for language in languages:
                    JobPostingLanguageRelation.objects.create(
                        job_posting=job_posting, language_id=language.get('language'),
                        language_level_id=language.get('language_level'))
        else:
            for obj in job_postings:
                try:
                    job_posting = JobPostingModel.objects.get(
                        slug=obj.get('slug'))
                except JobPostingModel.DoesNotExist:
                    job_posting = JobPostingModel(branch_id=obj.get('branch'), job_type_id=obj.get('job_type'),
                                                  company=company)
                job_title = obj.get('title', None)
                if job_title is None:
                    job_title = self.rand.title()
                job_posting.title = job_title
                job_posting.description = obj.get('description')
                workload = obj.get('workload')
                if workload is None or workload == '':
                    workload = self.rand.workload()
                job_posting.workload = workload
                job_posting.job_from_date = obj.get('job_from_date')
                job_posting.job_to_date = obj.get('job_to_date')
                job_posting.url = obj.get('url')
                job_posting.url = obj.get('url')
                job_posting.form_step = obj.get('form_step')
                job_posting.state = obj.get('state')
                job_posting.employee = get_user_model().objects.get(email=obj.get('employee')).employee
                job_posting.save()
                job_posting.slug = f'{slugify(job_posting.title)}-{str(job_posting.id)}'
                job_posting.save()
                job_posting.skills.set(obj.get('skills'))
                job_posting.job_requirements.set(obj.get('job_requirements'))

                languages = obj.get('languages')
                for language in languages:
                    try:
                        rel = JobPostingLanguageRelation.objects.get(job_posting=job_posting,
                                                                     language_id=language.get('language'))
                        rel.language_level_id = language.get('language_level')
                        rel.save()
                    except JobPostingLanguageRelation.DoesNotExist:
                        JobPostingLanguageRelation.objects.create(job_posting=job_posting,
                                                                  language_id=language.get('language'),
                                                                  language_level_id=language.get('language_level'))

    def random(self, *args, **kwargs):
        pass
