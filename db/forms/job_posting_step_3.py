from django import forms
from django.shortcuts import get_object_or_404

from db.exceptions import FormException
from db.helper.forms import validate_company_user_type, validate_job_posting_step, validate_form_data
from db.models import JobPosting, JobPostingState


class JobPostingFormStep3(forms.Form):
    state = forms.ChoiceField(choices=JobPostingState.choices)


def process_job_posting_form_step_3(user, data):
    errors = {}

    # validate user type, step and data
    validate_company_user_type(user)
    validate_form_data(data)
    job_posting = get_object_or_404(JobPosting, id=data.get('id'))
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
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update job posting
    if job_posting.form_step == 3:
        job_posting.form_step = 4

    job_posting.save()

    return job_posting
