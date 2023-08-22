from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_form_data, validate_company_user_type
from db.models import Benefit, ProfileType, Branch


class CompanyProfileAdvantagesForm(forms.Form):
    branches = forms.ModelMultipleChoiceField(queryset=Branch.objects.all(), required=False)
    benefits = forms.ModelMultipleChoiceField(queryset=Benefit.objects.all(), required=False)


def process_company_advantages_form(user, data):
    # validate user type, data
    errors = {}
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_form_data(data)
    company = user.company

    benefits_to_save = None
    branches_to_save = None

    # validate profile data
    form = CompanyProfileAdvantagesForm(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        # optional parameters
        branches_to_save = cleaned_data.get('branches')
        benefits_to_save = cleaned_data.get('benefits')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # save company
    company.save()
    company.benefits.set(benefits_to_save)
    company.branches.set(branches_to_save)
