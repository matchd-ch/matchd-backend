from django import forms
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper.forms import convert_object_to_id, validate_company_type, validate_form_data, convert_date, \
    generic_error_dict
from db.models import JobOption, JobPosting


class JobPostingFormStep1(forms.Form):
    description = forms.CharField(max_length=1000, required=True)
    job_option = forms.ModelChoiceField(queryset=JobOption.objects.all(), required=True)
    workload = forms.CharField(max_length=255, required=True)
    job_from_date = forms.DateField(required=True)
    job_to_date = forms.DateField(required=False)
    url = forms.URLField(required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['job_option'] = convert_object_to_id(data.get('job_option', None))
        data['job_from_date'] = convert_date(data.get('job_from_date', None), '%m.%Y')
        to_date = data.get('job_to_date', None)
        if to_date is not None:
            data['job_to_date'] = convert_date(data.get('job_to_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)


def process_job_posting_form_step_1(user, data):
    errors = {}

    validate_company_type(user)
    # todo validate step ?
    validate_form_data(data)

    form = JobPostingFormStep1(data)
    form.full_clean()

    if form.is_valid():
        cleaned_data = form.cleaned_data

        # validate date range
        from_date = cleaned_data.get('job_from_date')
        to_date = cleaned_data.get('job_to_date', None)

        if to_date is not None and from_date >= to_date:
            errors.update(generic_error_dict('job_to_date', _('Date must be after from date'),
                                             'invalid_range'))
        else:
            cleaned_data['company'] = user.company
            job_posting = JobPosting.objects.create(**cleaned_data)

    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)
