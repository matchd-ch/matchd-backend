from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type, convert_object_to_id
from db.models import Branch, UserType


class UniversityProfileFormStep2(forms.Form):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    description = forms.CharField(max_length=1000, required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['branch'] = convert_object_to_id(data.get('branch', None))
        super().__init__(data=data, **kwargs)


def process_university_form_step_2(user, data):
    # validate user type, step and data
    validate_company_user_type(user, UserType.UNIVERSITY)
    validate_step(user, 2)
    validate_form_data(data)
    errors = {}
    company = user.company

    # validate profile data
    form = UniversityProfileFormStep2(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        company.branch = cleaned_data.get('branch')
        company.description = cleaned_data.get('description')
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
