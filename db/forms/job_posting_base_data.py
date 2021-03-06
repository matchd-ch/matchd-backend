import requests
from django import forms
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
    description = forms.CharField(max_length=1000, required=False)
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all(), required=True)
    branches = forms.ModelMultipleChoiceField(queryset=Branch.objects.all(), required=True)
    workload = forms.IntegerField(required=True,
                                  validators=[MaxValueValidator(100),
                                              MinValueValidator(10)])
    job_from_date = forms.DateField(required=True)
    job_to_date = forms.DateField(required=False)
    url = forms.URLField(required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['job_type'] = convert_object_to_id(data.get('job_type', None))
        data['job_from_date'] = convert_date(data.get('job_from_date', None), '%m.%Y')
        to_date = data.get('job_to_date', None)
        if to_date is not None:
            data['job_to_date'] = convert_date(data.get('job_to_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)


# noinspection PyBroadException
def validate_html_url(url):
    try:
        response = requests.head(url)
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
        from_date = cleaned_data.get('job_from_date')
        to_date = cleaned_data.get('job_to_date', None)
        url = cleaned_data.get('url', None)

        if url is not None and url != '':
            if not validate_html_url(url):
                errors.update(
                    generic_error_dict('url', _('URL must point to a html page'), 'invalid'))

        if to_date is not None and from_date >= to_date:
            errors.update(
                generic_error_dict('job_to_date', _('Date must be after from date'),
                                   'invalid_range'))
        cleaned_data['job_from_date'] = from_date
        cleaned_data['job_to_date'] = to_date
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
    job_posting.workload = cleaned_data.get('workload', None)
    job_posting.job_from_date = cleaned_data.get('job_from_date')
    job_posting.job_to_date = cleaned_data.get('job_to_date', None)
    job_posting.url = cleaned_data.get('url', None)
    job_posting.company = cleaned_data.get('company')
    job_posting.save()
    job_posting.branches.set(cleaned_data.get('branches'))

    job_posting.slug = f'{slugify(job_posting.title)}-{str(job_posting.id)}'
    job_posting.save()

    return job_posting
