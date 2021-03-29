from django import forms
from django.utils.translation import gettext as _
from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type, generic_error_dict
from db.models import SoftSkill, ProfileState


class CompanyProfileFormStep4(forms.Form):
    soft_skills = forms.ModelMultipleChoiceField(queryset=SoftSkill.objects.all(), required=True)


def process_company_form_step_4(user, data):
    # validate user type, step and data
    errors = {}
    validate_company_user_type(user)
    validate_step(user, 4)
    validate_form_data(data)
    company = user.company

    soft_skills_to_save = None

    # validate profile data
    form = CompanyProfileFormStep4(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data
        soft_skills_to_save = cleaned_data.get('soft_skills')
        # check if more than 6 soft skills has been selected
        if len(list(soft_skills_to_save)) > 6:
            errors.update(generic_error_dict('softSkills', _('Too many Skills'), 'too_many_items'))

        # check if less than 6 soft skills has been selected
        if len(list(soft_skills_to_save)) < 6:
            errors.update(generic_error_dict('softSkills', _('Too few Skills'), 'too_few_items'))

    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 4
    if company.profile_step == 4:
        company.profile_step = 5

    # save user / profile
    company.state = ProfileState.PUBLIC
    user.save()
    company.soft_skills.set(soft_skills_to_save)
    company.save()
