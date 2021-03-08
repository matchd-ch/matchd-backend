from django.shortcuts import get_object_or_404
from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_company_type, validate_form_data, validate_job_posting_step, generic_error_dict
from db.models import JobPosting, Expectation, Skill


class JobPostingFormStep2(forms.Form):
    expectations = forms.ModelMultipleChoiceField(queryset=Expectation.objects.all(), required=False)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False)


def process_job_posting_form_step_2(user, data):
    errors = {}

    validate_company_type(user)
    validate_form_data(data)
    job_posting = get_object_or_404(JobPosting, id=data.get('id'))
    validate_job_posting_step(job_posting, 2)

    form = JobPostingFormStep2(data)
    form.full_clean()
    expectations_to_save = None
    skills_to_save = None

    if form.is_valid():
        cleaned_data = form.cleaned_data

        expectations_to_save = cleaned_data.get('expectations')
        skills_to_save = cleaned_data.get('skills')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    job_posting.expectations.set(expectations_to_save)
    job_posting.skills.set(skills_to_save)

    return job_posting
