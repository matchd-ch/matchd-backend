from django import forms

from db.exceptions import FormException
from db.helper import validate_student_user_type, validate_step, validate_form_data, generic_error_dict
from db.models.user import ProfileState


class StudentProfileConditionForm(forms.Form):
    state = forms.ChoiceField(choices=ProfileState.choices)


def process_student_condition_form(user, data):
    errors = {}

    # validate user type, step and data
    validate_student_user_type(user)
    validate_step(user, 6)
    validate_form_data(data)

    # do not disable enum conversion as described here:
    # https://docs.graphene-python.org/projects/django/en/latest/queries/#choices-to-enum-conversion
    # otherwise the frontend application will not have an enum type for the state field
    # force lower case of the input (eg. "INCOMPLETE", etc)
    data['state'] = data.get('state').lower()

    student = user.student

    form = StudentProfileConditionForm(data)
    form.full_clean()
    if form.is_valid():
        # update user profile
        cleaned_data = form.cleaned_data
        new_state = cleaned_data.get('state')
        if new_state not in (ProfileState.PUBLIC, ProfileState.ANONYMOUS):
            errors.update(
                generic_error_dict('state', 'Only public and anonymous are allowed', 'invalid'))
        student.state = new_state
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 6
    if student.profile_step == 6:
        student.profile_step = 7

    # save user
    student.save()
