from django import forms

from db.exceptions import FormException
from db.forms.hobby import HobbyForm
from db.forms.distinction import DistinctionForm
from db.forms.online_project import OnlineProjectForm
from db.forms.user_language_relation import UserLanguageRelationForm

from db.helper import validate_user_type, validate_step, validate_form_data, silent_fail
from db.models import Skill, OnlineProject


class StudentProfileFormStep4(forms.Form):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=True)


def process_hobby(data):
    if 'id' in data:
        return None
    form = HobbyForm(data)
    form.full_clean()
    if form.is_valid():
        return form
    errors = form.errors.get_json_data()
    if not silent_fail(errors):
        raise FormException(errors=errors)
    return None


def process_distinction(data):
    if 'id' in data:
        return None
    form = DistinctionForm(data)
    form.full_clean()
    if form.is_valid():
        return form
    errors = form.errors.get_json_data()
    if not silent_fail(errors):
        raise FormException(errors=errors)
    return None


def process_online_project(profile, data):
    if 'id' in data:
        return None

    form = OnlineProjectForm(data)
    form.full_clean()
    if form.is_valid():
        # OnlineProject Model fields (url and user) can't be unique together because url is too long
        # This is why we do a manual check
        if not OnlineProject.objects.filter(url=data['url'], student=profile).exists():
            return form
    else:
        raise FormException(errors=form.errors.get_json_data())
    return None


def process_language(data):
    if 'id' in data:
        return None

    form = UserLanguageRelationForm(data)
    form.full_clean()
    if form.is_valid():
        return form
    errors = form.errors.get_json_data()
    if not silent_fail(errors):
        raise FormException(errors=errors)
    return None


# pylint:disable=R0912
def process_student_form_step_4(user, data):
    # validate user type, step and data
    validate_user_type(user)
    validate_step(user, 4)
    validate_form_data(data)

    errors = {}

    profile = user.student

    # validate profile data
    profile_form = StudentProfileFormStep4(data)
    profile_form.full_clean()
    skills_to_save = None

    if profile_form.is_valid():
        # update user / profile
        profile_data_for_update = profile_form.cleaned_data
        skills_to_save = profile_data_for_update.get('skills')
    else:
        errors.update(profile_form.errors.get_json_data())

    # validate hobbies
    hobbies = data.get('hobbies', None)
    valid_hobby_forms = []
    for hobby in hobbies:
        hobby['student'] = profile.id
        try:
            valid_hobby_forms.append(process_hobby(hobby))
        except FormException as exception:
            errors.update(exception.errors)

    # validate distinctions
    distinctions = data.get('distinctions', None)
    valid_distinction_forms = []
    for distinction in distinctions:
        distinction['student'] = profile.id
        try:
            valid_distinction_forms.append(process_distinction(distinction))
        except FormException as exception:
            errors.update(exception.errors)

    # validate online projects
    online_projects = data.get('online_projects', None)
    valid_online_project_forms = []
    for online_project in online_projects:
        online_project['student'] = profile.id
        try:
            valid_online_project_forms.append(process_online_project(profile, online_project))
        except FormException as exception:
            errors.update(exception.errors)

    # validate languages
    languages = data.get('languages', None)
    valid_languages_forms = []
    for language in languages:
        language['student'] = profile.id
        try:
            valid_languages_forms.append(process_language(language))
        except FormException as exception:
            errors.update(exception.errors)

    if errors:
        raise FormException(errors=errors)

    # save all valid forms
    valid_forms = valid_hobby_forms + valid_distinction_forms + valid_online_project_forms + valid_languages_forms
    for form in valid_forms:
        form.save()

    profile.skills.set(skills_to_save)

    # update step only if the user has step 4
    if user.profile_step == 4:
        user.profile_step = 5

    # save user
    user.save()
