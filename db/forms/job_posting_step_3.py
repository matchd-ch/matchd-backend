import datetime

from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper.forms import validate_company_user_type, validate_job_posting_step, validate_form_data, \
    convert_object_to_id, generic_error_dict
from db.models import JobPosting, JobPostingState, Employee


class JobPostingFormStep3(forms.Form):
    state = forms.ChoiceField(choices=JobPostingState.choices)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['employee'] = convert_object_to_id(data.get('employee', None))
        super().__init__(data=data, **kwargs)


def process_job_posting_form_step_3(user, data):
    errors = {}

    # validate user type, step and data
    validate_company_user_type(user)
    validate_form_data(data)
    job_posting = get_object_or_404(JobPosting, id=data.get('id'))
    is_published = job_posting.state == JobPostingState.PUBLIC
    validate_job_posting_step(job_posting, 3)

    # do not disable enum conversion as described here:
    # https://docs.graphene-python.org/projects/django/en/latest/queries/#choices-to-enum-conversion
    # otherwise the frontend application will not have an enum type for the state field
    # force lower case of the input (eg. "DRAFT", etc)
    data['state'] = data.get('state').lower()

    form = JobPostingFormStep3(data)
    form.full_clean()
    if form.is_valid():
        # update job posting
        cleaned_data = form.cleaned_data
        job_posting.state = cleaned_data.get('state')
        job_posting.employee = cleaned_data.get('employee')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # pylint: disable=W0511
    # TODO create validator
    # check if employee belongs to the same company
    user_company = user.company.id
    job_posting_company = job_posting.company.id
    if user_company != job_posting_company:
        errors.update(generic_error_dict('employee', _('Employee does not belong to this company.'), 'invalid'))
        raise FormException(errors=errors)

    # update job posting
    if job_posting.form_step == 3:
        job_posting.form_step = 4

    job_posting.save()

    if not is_published and job_posting.state == JobPostingState.PUBLIC:
        job_posting.date_published = datetime.datetime.now()
        job_posting.save()

    return job_posting
