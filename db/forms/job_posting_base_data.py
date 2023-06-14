import requests
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper.forms import convert_object_to_id, validate_company_user_type, validate_form_data, convert_date, \
    generic_error_dict
from db.models import JobType, JobPosting, Branch


class JobPostingBaseDataForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=3000, required=False)
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all(), required=True)
    branches = forms.ModelMultipleChoiceField(queryset=Branch.objects.all(), required=True)
    workload_from = forms.IntegerField(required=True,
                                       validators=[MaxValueValidator(100),
                                                   MinValueValidator(10)])
    workload_to = forms.IntegerField(required=True,
                                     validators=[MaxValueValidator(100),
                                                 MinValueValidator(10)])
    job_from_date = forms.DateField(required=False)
    job_to_date = forms.DateField(required=False)
    job_period_by_agreement = forms.BooleanField(required=False)
    url = forms.URLField(required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['job_type'] = convert_object_to_id(data.get('job_type', None))

        data['job_period_by_agreement'] = data.get('job_period_by_agreement', False)
        data['job_from_date'] = convert_date(data.get('job_from_date', None), '%m.%Y')
        data['job_to_date'] = convert_date(data.get('job_to_date', None), '%m.%Y')

        super().__init__(data=data, **kwargs)

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        self.validate_workload(cleaned_data)
        self.validate_work_period(cleaned_data)

    def validate_workload(self, cleaned_data):
        workload_from = cleaned_data.get('workload_from')
        workload_to = cleaned_data.get('workload_to')

        if workload_from is None:
            raise ValidationError({'workload_from': "Must be provided."})

        if workload_to is None:
            raise ValidationError({'workload_to': "Must be provided."})

        if workload_from > workload_to:
            raise ValidationError(
                {'workload_to': "Workload to must be greated than workload from."})

    def validate_work_period(self, cleaned_data):
        job_from_date = cleaned_data.get('job_from_date')
        job_to_date = cleaned_data.get('job_to_date')
        job_period_by_agreement = cleaned_data.get('job_period_by_agreement')

        if job_period_by_agreement:
            if job_from_date is not None:
                raise ValidationError(
                    {'job_from_date': "Must be empty if job period is by agreement."})

            if job_to_date is not None:
                raise ValidationError(
                    {'job_to_date': "Must be empty if job period is by agreement."})
        else:
            if job_from_date is None and job_to_date is None:
                raise ValidationError([
                    ValidationError(
                        'job_from_date',
                        code=
                        "Either from date or to date must be set if the job period is not by agreement."
                    ),
                    ValidationError(
                        'job_to_date',
                        code=
                        "Either from date or to date must be set if the job period is not by agreement."
                    )
                ])

            if job_from_date is not None and job_to_date is not None and job_from_date > job_to_date:
                raise ValidationError(
                    {'job_to_date': "Job from date to must be greated than job to date."})


# noinspection PyBroadException
def validate_html_url(url):
    try:
        response = requests.head(url, timeout=10)
        content_type = response.headers.get('Content-Type')
        return 'text/html' in content_type
    except Exception:
        return False


def process_job_posting_base_data_form(user, data):
    errors = {}

    validate_company_user_type(user)
    validate_form_data(data)

    form = JobPostingBaseDataForm(data)
    form.full_clean()

    cleaned_data = None

    # pylint: disable=W0511
    # TODO create validator
    url = data.get('url')
    if url is not None and url != '':
        if 'http' not in url:
            url = f'http://{url}'
        if not validate_html_url(url):
            errors.update(generic_error_dict('url', _('URL must point to a html page'), 'invalid'))

    if form.is_valid():
        cleaned_data = form.cleaned_data

        # validate date range
        url = cleaned_data.get('url', None)

        if url is not None and url != '':
            if not validate_html_url(url):
                errors.update(
                    generic_error_dict('url', _('URL must point to a html page'), 'invalid'))

        cleaned_data['company'] = user.company
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # get existing job posting
    job_posting_id = data.get('id', None)
    if job_posting_id is not None:
        job_posting = get_object_or_404(JobPosting, pk=job_posting_id)
    else:
        job_posting = JobPosting()

    job_posting.title = cleaned_data.get('title')
    job_posting.description = cleaned_data.get('description')
    job_posting.job_type = cleaned_data.get('job_type')
    job_posting.workload_from = cleaned_data.get('workload_from')
    job_posting.workload_to = cleaned_data.get('workload_to')
    job_posting.job_from_date = cleaned_data.get('job_from_date', None)
    job_posting.job_to_date = cleaned_data.get('job_to_date', None)
    job_posting.job_period_by_agreement = cleaned_data.get('job_period_by_agreement')
    job_posting.url = cleaned_data.get('url', None)
    job_posting.company = cleaned_data.get('company')
    job_posting.save()
    job_posting.branches.set(cleaned_data.get('branches'))

    job_posting.slug = f'{slugify(job_posting.title)}-{str(job_posting.id)}'
    job_posting.save()

    return job_posting
