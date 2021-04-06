from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type
from db.models import Branch, ProfileType


class UniversityProfileFormStep2(forms.Form):
    branches = forms.ModelMultipleChoiceField(queryset=Branch.objects.all(), required=False)
    description = forms.CharField(max_length=1000, required=False)


def process_university_form_step_2(user, data):
    # validate user type, step and data
    validate_company_user_type(user, ProfileType.UNIVERSITY)
    validate_step(user, 2)
    validate_form_data(data)
    errors = {}
    company = user.company
    branches_to_save = None

    # validate profile data
    form = UniversityProfileFormStep2(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        branches_to_save = cleaned_data.get('branches')
        company.description = cleaned_data.get('description')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 2
    if company.profile_step == 2:
        company.profile_step = 3

    # save user / profile
    company.branches.set(branches_to_save)
    user.save()
    company.save()
