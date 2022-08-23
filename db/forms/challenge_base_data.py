from django import forms
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from db.exceptions import FormException
from db.helper.forms import convert_object_to_id, validate_form_data
from db.models import ChallengeType, Keyword, Challenge, ProfileType


class ChallengeBaseDataForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=1500, required=True)
    team_size = forms.IntegerField(min_value=1, required=True)
    compensation = forms.CharField(max_length=300, required=True)
    challenge_type = forms.ModelChoiceField(queryset=ChallengeType.objects.all(), required=True)
    keywords = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all(), required=True)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['challenge_type'] = convert_object_to_id(data.get('challenge_type', None))
        super().__init__(data=data, **kwargs)


def process_challenge_base_data_form(user, data):
    errors = {}

    validate_form_data(data)

    form = ChallengeBaseDataForm(data)
    form.full_clean()

    cleaned_data = None

    if form.is_valid():
        cleaned_data = form.cleaned_data
        if user.type in ProfileType.valid_company_types():
            cleaned_data['company'] = user.company
            cleaned_data['employee'] = user.employee
        if user.type in ProfileType.valid_student_types():
            cleaned_data['student'] = user.student
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # get existing job posting
    challenge_id = data.get('id', None)
    if challenge_id is not None:
        challenge = get_object_or_404(Challenge, pk=challenge_id)
    else:
        challenge = Challenge()

    challenge.title = cleaned_data.get('title')
    challenge.description = cleaned_data.get('description')
    challenge.team_size = cleaned_data.get('team_size')
    challenge.compensation = cleaned_data.get('compensation')
    challenge.challenge_type = cleaned_data.get('challenge_type')
    challenge.company = cleaned_data.get('company')
    challenge.student = cleaned_data.get('student')
    challenge.employee = cleaned_data.get('employee')
    challenge.save()
    challenge.keywords.set(cleaned_data.get('keywords'))

    challenge.slug = f'{slugify(challenge.title)}-{str(challenge.id)}'
    challenge.save()
    return challenge
