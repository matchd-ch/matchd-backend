from django import forms
from django.core.exceptions import ValidationError

from db.exceptions import FormException, NicknameException
from db.helper import validation_error_to_dict, \
    validate_student_type, validate_step, validate_form_data, NicknameHelper


class StudentProfileFormStep5(forms.Form):
    nickname = forms.CharField(max_length=150)


def process_student_form_step_5(user, data):
    errors = {}
    # validate user type, step and data
    validate_student_type(user)
    validate_step(user, 5)
    validate_form_data(data)

    profile = None
    form = StudentProfileFormStep5(data)
    form.full_clean()
    if form.is_valid():
        # update user profile
        cleaned_data = form.cleaned_data
        profile = user.student

        nickname = cleaned_data.get('nickname')
        nickname_helper = NicknameHelper()
        try:
            nickname_helper.validate(user, nickname)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'nickname'))
            suggestions = nickname_helper.get_suggestions(user, nickname)
            # pylint:disable=W0707
            raise NicknameException(errors=errors, suggestions=suggestions)

        profile.nickname = cleaned_data.get('nickname')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 6
    if user.profile_step == 5:
        user.profile_step = 6

    # save user / profile
    user.save()
    profile.save()
