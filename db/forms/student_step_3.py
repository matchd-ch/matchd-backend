from django import forms
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper import validate_student_user_type, validate_step, validate_form_data, generic_error_dict
from db.models import SoftSkill, CulturalFit


class StudentProfileFormStep3(forms.Form):
    soft_skills = forms.ModelMultipleChoiceField(queryset=SoftSkill.objects.all(), required=True)
    cultural_fits = forms.ModelMultipleChoiceField(queryset=CulturalFit.objects.all(), required=True)


def process_student_form_step_3(user, data):
    errors = {}
    # validate user type, step and data
    validate_student_user_type(user)
    validate_step(user, 3)
    validate_form_data(data)

    student = None
    form = StudentProfileFormStep3(data)
    form.full_clean()
    soft_skills_to_save = None
    cultural_fits_to_save = None

    if form.is_valid():
        # update user profile
        student = user.student
        cleaned_data = form.cleaned_data

        # required parameters
        soft_skills_to_save = cleaned_data.get('soft_skills')

        # check if more than 6 soft skills has been selected
        if len(list(soft_skills_to_save)) > 6:
            errors.update(generic_error_dict('softSkills', _('Too many skills'), 'too_many_items'))

        # check if less than 6 soft skills has been selected
        if len(list(soft_skills_to_save)) < 6:
            errors.update(generic_error_dict('softSkills', _('Too few skills'), 'too_few_items'))

        cultural_fits_to_save = cleaned_data.get('cultural_fits')

        # check if more than 6 cultural fits has been selected
        if len(list(cultural_fits_to_save)) > 6:
            errors.update(generic_error_dict('culturalFits', _('Too many cultural fits'), 'too_many_items'))

        # check if less than 6 cultural fits has been selected
        if len(list(cultural_fits_to_save)) < 6:
            errors.update(generic_error_dict('culturalFits', _('Too few cultural fits'), 'too_few_items'))

    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    student.soft_skills.set(soft_skills_to_save)
    student.cultural_fits.set(cultural_fits_to_save)

    # update step only if the user has step 3
    if student.profile_step == 3:
        student.profile_step = 4

    # save user / profile
    student.save()
