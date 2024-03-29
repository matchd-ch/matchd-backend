from django import forms
from django.utils.translation import gettext as _
from db.exceptions import FormException
from db.helper.forms import validate_form_data, validate_company_user_type, generic_error_dict
from db.models import SoftSkill, CulturalFit


class CompanyProfileValuesForm(forms.Form):
    soft_skills = forms.ModelMultipleChoiceField(queryset=SoftSkill.objects.all(), required=False)
    cultural_fits = forms.ModelMultipleChoiceField(queryset=CulturalFit.objects.all(),
                                                   required=False)


def process_company_values_form(user, data):
    # validate user type, data
    errors = {}
    validate_company_user_type(user)
    validate_form_data(data)
    company = user.company

    soft_skills_to_save = None
    cultural_fits_to_save = None

    # validate profile data
    form = CompanyProfileValuesForm(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        soft_skills_to_save = cleaned_data.get('soft_skills')
        # check if more than 6 soft skills has been selected
        if len(list(soft_skills_to_save)) > 6:
            errors.update(generic_error_dict('softSkills', _('Too many skills'), 'too_many_items'))

        cultural_fits_to_save = cleaned_data.get('cultural_fits')
        # check if more than 6 cultural fits has been selected
        if len(list(cultural_fits_to_save)) > 6:
            errors.update(
                generic_error_dict('culturalFits', _('Too many cultural fits'), 'too_many_items'))

    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # save user / profile
    user.save()
    company.soft_skills.set(soft_skills_to_save)
    company.cultural_fits.set(cultural_fits_to_save)
    company.save()
