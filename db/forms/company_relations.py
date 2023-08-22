from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_form_data, validate_company_user_type
from db.models import ProfileType


class CompanyProfileRelationsForm(forms.Form):
    website = forms.URLField(max_length=2048, required=False)
    description = forms.CharField(max_length=3000, required=False)
    services = forms.CharField(max_length=3000, required=False)
    # Bug prevention, when false is given as parameter
    member_it_st_gallen = forms.BooleanField(required=False, initial=False)


def process_company_relations_form(user, data):
    # validate user type, data
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_form_data(data)
    errors = {}
    company = user.company

    # validate profile data
    form = CompanyProfileRelationsForm(data)
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

    # save user / profile
    user.save()
    company.save()
