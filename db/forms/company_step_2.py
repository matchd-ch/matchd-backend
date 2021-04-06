from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type
from db.models import ProfileType


class CompanyProfileFormStep2(forms.Form):
    website = forms.URLField(max_length=2048, required=True)
    description = forms.CharField(max_length=1000, required=False)
    services = forms.CharField(max_length=1000, required=False)
    # Bug prevention, when false is given as parameter
    member_it_st_gallen = forms.BooleanField(required=False, initial=False)


def process_company_form_step_2(user, data):
    # validate user type, step and data
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_step(user, 2)
    validate_form_data(data)
    errors = {}
    company = user.company

    # validate profile data
    form = CompanyProfileFormStep2(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        # required parameters
        company.website = cleaned_data.get('website')
        company.member_it_st_gallen = cleaned_data.get('member_it_st_gallen')

        # optional parameters
        company.description = cleaned_data.get('description')
        company.services = cleaned_data.get('services')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 2
    if company.profile_step == 2:
        company.profile_step = 3

    # save user / profile
    user.save()
    company.save()
