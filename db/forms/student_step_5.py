from django import forms
from django.core.exceptions import ValidationError

from db.exceptions import FormException, NicknameException
from db.helper import validate_user_type_step_and_data, validation_error_to_dict, NicknameSuggestions
from db.validators import NicknameValidator


class StudentProfileFormStep5(forms.Form):
    nickname = forms.CharField(max_length=150)


def process_student_form_step_5(user, data):
    errors = {}
    # validate user type, step and data
    validate_user_type_step_and_data(user, data, 5)

    profile = None
    form = StudentProfileFormStep5(data)
    form.full_clean()
    if form.is_valid():
        # update user profile
        cleaned_data = form.cleaned_data
        profile = user.student

        nickname = cleaned_data.get('nickname')
        try:
            nickname_validator = NicknameValidator()
            nickname_validator.validate(user, nickname)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'nickname'))
            nicknames = NicknameSuggestions()
            suggestions = nicknames.get_suggestions(user, nickname)
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
