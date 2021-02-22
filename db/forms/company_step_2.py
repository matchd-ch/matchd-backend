from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_user_type, validate_step, validate_form_data


class CompanyProfileFormStep2(forms.Form):
    website = forms.URLField(max_length=255, required=True)
    branch = forms.IntegerField(required=False)
    description = forms.CharField(max_length=1000, required=False)
    services = forms.CharField(max_length=1000, required=False)
    member_it_st_gallen = forms.BooleanField(required=True)


def process_company_form_step_2(user, data):
    errors = {}
    validate_user_type(user, 'company')
    validate_step(user, 2)
    validate_form_data(data)
    profile = user.company
    form = CompanyProfileFormStep2(data)
    form.full_clean()
    if form.is_valid():
        profile = user.company
        cleaned_data = form.cleaned_data
        profile.website = cleaned_data.get('website')
        profile.branch = cleaned_data.get('branch')
        profile.description = cleaned_data.get('description')
        profile.services = cleaned_data.get('services')
        profile.member_it_st_gallen = cleaned_data.get('member_it_st_gallen')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 2
    if user.profile_step == 2:
        user.profile_step = 3

    # save user / profile
    user.save()
    profile.save()
