from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type
from db.models import JobPosition, Benefit, ProfileType


class CompanyProfileFormStep3(forms.Form):
    job_positions = forms.ModelMultipleChoiceField(queryset=JobPosition.objects.all(), required=False)
    benefits = forms.ModelMultipleChoiceField(queryset=Benefit.objects.all(), required=False)


def process_company_form_step_3(user, data):
    # validate user type, step and data
    errors = {}
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_step(user, 3)
    validate_form_data(data)
    company = user.company

    benefits_to_save = None
    job_positions_to_save = None

    # validate profile data
    form = CompanyProfileFormStep3(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        # optional parameters
        job_positions_to_save = cleaned_data.get('job_positions')
        benefits_to_save = cleaned_data.get('benefits')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 3
    if company.profile_step == 3:
        company.profile_step = 4

    # save company
    company.save()
    company.benefits.set(benefits_to_save)
    company.job_positions.set(job_positions_to_save)
