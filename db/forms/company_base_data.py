from django import forms
from django.conf import settings
from django.core.validators import RegexValidator

from db.exceptions import FormException
from db.helper import validate_form_data
from db.helper.forms import validate_company_user_type
from db.models import ProfileType


class CompanyProfileBaseDataForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    name = forms.CharField(max_length=255, required=False)
    street = forms.CharField(max_length=255, required=False)
    zip = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    phone = forms.CharField(max_length=12,
                            validators=[RegexValidator(regex=settings.PHONE_REGEX)],
                            required=False)
    role = forms.CharField(max_length=255, required=False)


def process_company_base_data_form(user, data):
    # validate user type, data
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_form_data(data)
    errors = {}
    company = user.company
    employee = user.employee

    # validate profile data
    form = CompanyProfileBaseDataForm(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        # required parameters
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        company.name = cleaned_data.get('name')
        company.street = cleaned_data.get('street')
        company.zip = cleaned_data.get('zip')
        company.city = cleaned_data.get('city')
        company.phone = cleaned_data.get('phone')
        employee.role = cleaned_data.get('role')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # save user / company / employee
    user.save()
    company.save()
    employee.save()
