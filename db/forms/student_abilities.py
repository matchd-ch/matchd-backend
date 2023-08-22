from django import forms
from django.db.models import Q

from db.exceptions import FormException
from db.forms.hobby import HobbyForm
from db.forms.online_challenge import OnlineChallengeForm
from db.forms.user_language_relation import UserLanguageRelationForm

from db.helper import validate_student_user_type, validate_form_data, silent_fail, generic_error_dict
from db.models import Skill, OnlineChallenge, Hobby, UserLanguageRelation


class StudentProfileAbilitiesForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False)
    distinction = forms.CharField(max_length=3000, required=False)


def get_language_relation_instance_or_none(student, model, data):
    instance = None
    object_id = data.get('id', None)
    query = None
    if object_id is not None:
        query = Q(pk=object_id)
    else:
        language_id = data.get('language')
        if language_id is not None:
            query = Q(language_id=language_id, student=student)
    try:
        instance = model.objects.get(query)
    except model.DoesNotExist:
        pass
    return instance


def get_instance_or_none(model, data):
    object_id = data.get('id', None)
    if object_id is None:
        return None
    instance = None
    try:
        instance = model.objects.get(pk=object_id)
    except model.DoesNotExist:
        pass
    return instance


def process_hobby(data):
    instance = get_instance_or_none(Hobby, data)
    form = HobbyForm(data, instance=instance)
    form.full_clean()
    if form.is_valid():
        return form
    errors = form.errors.get_json_data()
    if not silent_fail(errors) or instance is not None:
        raise FormException(errors=errors)
    return None


def get_hobbies_to_delete(profile, data):
    exclude_ids = []
    if data is not None:
        for hobby in data:
            if 'id' in hobby:
                exclude_ids.append(hobby.get('id'))
    return Hobby.objects.filter(student=profile).exclude(id__in=exclude_ids)


def challenge_url_already_exists(profile, url, instance=None):
    if instance is None:
        return OnlineChallenge.objects.filter(url=url, student=profile).exists()
    return OnlineChallenge.objects.filter(url=url, student=profile).exclude(pk=instance.id).exists()


def process_online_challenge(profile, data):
    instance = get_instance_or_none(OnlineChallenge, data)
    form = OnlineChallengeForm(data, instance=instance)
    form.full_clean()
    if form.is_valid():
        cleaned_data = form.cleaned_data
        # OnlineChallenge Model fields (url and user) can't be unique together because url is too long
        # This is why we do a manual check
        if not challenge_url_already_exists(profile, cleaned_data.get('url'), instance):
            return form
        if instance is not None:
            raise FormException(errors=generic_error_dict(
                'nonFieldErrors', 'A challenge with the same url already exists',
                'unique_together'))
    else:
        raise FormException(errors=form.errors.get_json_data())
    return None


def get_online_challenges_to_delete(profile, data):
    exclude_ids = []
    if data is not None:
        for online_challenge in data:
            if 'id' in online_challenge:
                exclude_ids.append(online_challenge.get('id'))
    return OnlineChallenge.objects.filter(student=profile).exclude(id__in=exclude_ids)


def process_language(student, data):
    instance = get_language_relation_instance_or_none(student, UserLanguageRelation, data)
    form = UserLanguageRelationForm(data, instance=instance)
    form.full_clean()
    if form.is_valid():
        return form
    errors = form.errors.get_json_data()
    if not silent_fail(errors):
        raise FormException(errors=errors)
    return None


def get_unique_languages(data):
    unique_languages = []
    languages = []
    for language in data:
        language_id = language.get('language')
        if language_id in languages:
            continue
        languages.append(language_id)
        unique_languages.append(language)
    return unique_languages


def get_languages_to_delete(profile, data):
    exclude_ids = []
    exclude_languages = []
    if data is not None:
        for language in data:
            if 'id' in language:
                exclude_ids.append(language.get('id'))
            if 'language' in language:
                exclude_languages.append(language.get('language'))
    languages_to_delete = UserLanguageRelation.objects.filter(student=profile)
    return languages_to_delete.exclude(id__in=exclude_ids).exclude(
        language_id__in=exclude_languages)


# pylint:disable=R0912
# pylint:disable=R0915
def process_student_abilities_form(user, data):
    # validate user type, data
    validate_student_user_type(user)
    validate_form_data(data)

    errors = {}
    student = user.student

    # validate profile data
    profile_form = StudentProfileAbilitiesForm(data)
    profile_form.full_clean()
    skills_to_save = None

    if profile_form.is_valid():
        # update user / profile
        profile_data_for_update = profile_form.cleaned_data
        skills_to_save = profile_data_for_update.get('skills')
        student.distinction = profile_data_for_update.get('distinction')
    else:
        errors.update(profile_form.errors.get_json_data())

    # validate hobbies
    hobbies = data.get('hobbies', None)
    hobbies_to_delete = get_hobbies_to_delete(student, hobbies)
    valid_hobby_forms = []
    if hobbies is not None:
        for hobby in hobbies:
            hobby['student'] = student.id
            try:
                hobby_form = process_hobby(hobby)
                if hobby_form is not None:
                    valid_hobby_forms.append(hobby_form)
            except FormException as exception:
                errors.update(exception.errors)

    # validate online challenges
    online_challenges = data.get('online_challenges', None)
    online_challenges_to_delete = get_online_challenges_to_delete(student, online_challenges)
    valid_online_challenge_forms = []
    if online_challenges is not None:
        for online_challenge in online_challenges:
            online_challenge['student'] = student.id
            try:
                online_challenge_form = process_online_challenge(student, online_challenge)
                if online_challenge_form is not None:
                    valid_online_challenge_forms.append(online_challenge_form)
            except FormException as exception:
                errors.update(exception.errors)

    # validate languages
    languages = data.get('languages', None)
    languages = get_unique_languages(languages)
    languages_to_delete = get_languages_to_delete(student, languages)
    valid_languages_forms = []
    if languages is not None:
        for language in languages:
            language['student'] = student.id
            try:
                language_form = process_language(student, language)
                if language_form is not None:
                    valid_languages_forms.append(language_form)
            except FormException as exception:
                errors.update(exception.errors)

    if errors:
        raise FormException(errors=errors)

    hobbies_to_delete.delete()
    online_challenges_to_delete.delete()
    languages_to_delete.delete()

    # save all valid forms
    valid_forms = valid_hobby_forms + valid_online_challenge_forms + valid_languages_forms
    for form in valid_forms:
        form.save()

    student.skills.set(skills_to_save)

    # save user
    user.save()
    student.save()
