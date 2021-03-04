from django import forms

from db.exceptions import FormException
from db.helper import validate_user_type, validate_step, validate_form_data
from db.models import UserState


class StudentProfileFormStep6(forms.Form):
    state = forms.ChoiceField(choices=UserState.choices)


def process_student_form_step_6(user, data):
    errors = {}

    # validate user type, step and data
    validate_user_type(user)
    validate_step(user, 6)
    validate_form_data(data)

    # do not disable enum conversion as described here:
    # https://docs.graphene-python.org/projects/django/en/latest/queries/#choices-to-enum-conversion
    # otherwise the frontend application will not have an enum type for the state field
    # force lower case of the input (eg. "INCOMPLETE", etc)
    data['state'] = data.get('state').lower()

    form = StudentProfileFormStep6(data)
    form.full_clean()
    if form.is_valid():
        # update user profile
        cleaned_data = form.cleaned_data
        user.state = cleaned_data.get('state')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 6
    if user.profile_step == 6:
        user.profile_step = 7

    # save user
    user.save()
