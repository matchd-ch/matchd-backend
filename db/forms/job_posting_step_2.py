import graphene
from django.shortcuts import get_object_or_404
from django import forms
from django.utils.translation import gettext as _

from api.schema.job_posting_language_relation import JobPostingLanguageRelationInput
from db.exceptions import FormException
from db.forms.job_posting_language_relation import JobPostingLanguageRelationForm
from db.helper.forms import validate_company_user_type, validate_form_data, validate_job_posting_step, silent_fail
from db.models import JobPosting, JobRequirement, Skill, JobPostingLanguageRelation, Language


class JobPostingFormStep2(forms.Form):
    job_requirements = forms.ModelMultipleChoiceField(queryset=JobRequirement.objects.all(), required=False)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False)
    languages = graphene.List(JobPostingLanguageRelationInput, description=_('Languages'), required=False)


def get_unique_languages(data):
    # only allow short list languages
    short_list_languages = Language.objects.filter(short_list=True).values_list('id', flat=True)
    unique_languages = []
    languages = []
    for language in data:
        language_id = language.get('language')
        if language_id in languages:
            continue
        languages.append(language_id)
        if int(language_id) in short_list_languages:
            unique_languages.append(language)
    return unique_languages


def get_languages_to_delete(job_posting, data):
    exclude_ids = []
    exclude_languages = []
    if data is not None:
        for language in data:
            if 'id' in language:
                exclude_ids.append(language.get('id'))
            if 'language' in language:
                exclude_languages.append(language.get('language'))
    languages_to_delete = JobPostingLanguageRelation.objects.filter(job_posting=job_posting)
    return languages_to_delete.exclude(id__in=exclude_ids).exclude(language_id__in=exclude_languages)


def process_language(job_posting, data):
    instance = None
    existing_entry_for_language = JobPostingLanguageRelation.objects.filter(job_posting=job_posting,
                                                                            language=data.get('language', None))

    if len(existing_entry_for_language) > 0:
        instance = existing_entry_for_language[0]
        data['id'] = instance.id

    form = JobPostingLanguageRelationForm(data, instance=instance)
    form.full_clean()
    if form.is_valid():
        return form
    errors = form.errors.get_json_data()
    if not silent_fail(errors):
        raise FormException(errors=errors)
    return None


def process_job_posting_form_step_2(user, data):
    errors = {}

    validate_company_user_type(user)
    validate_form_data(data)
    job_posting = get_object_or_404(JobPosting, id=data.get('id'))
    validate_job_posting_step(job_posting, 2)

    form = JobPostingFormStep2(data)
    form.full_clean()
    job_requirements_to_save = None
    skills_to_save = None

    if form.is_valid():
        cleaned_data = form.cleaned_data

        job_requirements_to_save = cleaned_data.get('job_requirements')
        skills_to_save = cleaned_data.get('skills')
    else:
        errors.update(form.errors.get_json_data())

    # validate languages
    languages = data.get('languages', None)
    valid_languages_forms = []
    languages_to_delete = None
    if languages is not None:
        languages = get_unique_languages(languages)
        languages_to_delete = get_languages_to_delete(job_posting, languages)
        for language in languages:
            language['job_posting'] = job_posting.id
            try:
                form = process_language(job_posting, language)
                if form is not None:
                    valid_languages_forms.append(form)
            except FormException as exception:
                errors.update(exception.errors)

    if errors:
        raise FormException(errors=errors)

    # save all valid forms
    for form in valid_languages_forms:
        form.save()

    # delete language that are no longer needed
    if languages_to_delete is not None:
        languages_to_delete.delete()

    job_posting.job_requirements.set(job_requirements_to_save)
    job_posting.skills.set(skills_to_save)

    if job_posting.form_step == 2:
        job_posting.form_step = 3

    job_posting.save()

    return job_posting
