from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type
from db.models import JobPosition


class CompanyProfileFormStep3(forms.Form):
    job_position = forms.ModelMultipleChoiceField(queryset=JobPosition.objects.all(), required=False)
    benefits = forms.CharField(required=False)


def process_company_form_step_3(user, data):
    # validate user type, step and data
    errors = {}
    validate_company_user_type(user)
    validate_step(user, 3)
    validate_form_data(data)
    profile = user.company

    # validate profile data
    form = CompanyProfileFormStep3(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        profile = user.company
        cleaned_data = form.cleaned_data

        # optional parameters
        profile.job_position = cleaned_data.get('job_position')
        profile.benefits = cleaned_data.get('benefits')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 3
    if user.profile_step == 3:
        user.profile_step = 4

    # save user / profile
    user.save()
    profile.save()
