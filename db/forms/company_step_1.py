from django import forms
from django.conf import settings
from django.core.validators import RegexValidator

from db.exceptions import FormException
from db.helper import validate_user_type, validate_step, validate_form_data


class CompanyProfileFormStep1(forms.Form):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    street = forms.CharField(max_length=255, required=True)
    zip = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=255, required=True)
    uid = forms.CharField(max_length=255, required=True,
                          validators=[RegexValidator(regex=r'CHE-[0-9]{3}.[0-9]{3}.[0-9]{3}')])
    phone = forms.CharField(max_length=12, validators=[RegexValidator(regex=settings.MOBILE_REGEX)], required=True)
    email = forms.EmailField(max_length=255, required=True)


def process_company_form_step_1(user, data):
    validate_user_type(user)
    validate_step(user, 1)
    validate_form_data(data)
    errors = {}
    profile = user.student
    form = CompanyProfileFormStep1(data)
    form.full_clean()
    if form.is_valid():
        cleaned_data = form.cleaned_data
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        user.uid = cleaned_data.get('uid')
        profile.street = cleaned_data.get('street')
        profile.zip = cleaned_data.get('zip')
        profile.city = cleaned_data.get('city')
        profile.phone = cleaned_data.get('phone')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)
    if user.profile_step == 1:
        user.profile_step = 2
    user.save()
    profile.save()
