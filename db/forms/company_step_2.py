from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type, convert_object_to_id
from db.models import Branch


class CompanyProfileFormStep2(forms.Form):
    website = forms.URLField(max_length=255, required=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    description = forms.CharField(max_length=1000, required=False)
    services = forms.CharField(max_length=1000, required=False)
    # Bug prevention, when false is given as parameter
    member_it_st_gallen = forms.BooleanField(required=False, initial=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['branch'] = convert_object_to_id(data.get('branch', None))
        super().__init__(data=data, **kwargs)


def process_company_form_step_2(user, data):
    # validate user type, step and data
    validate_company_user_type(user)
    validate_step(user, 2)
    validate_form_data(data)
    errors = {}
    profile = user.company

    # validate profile data
    form = CompanyProfileFormStep2(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        profile = user.company
        cleaned_data = form.cleaned_data

        # required parameters
        profile.website = cleaned_data.get('website')
        profile.member_it_st_gallen = cleaned_data.get('member_it_st_gallen')

        # optional parameters
        profile.branch = cleaned_data.get('branch')
        profile.description = cleaned_data.get('description')
        profile.services = cleaned_data.get('services')
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
