from django import forms
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from db.exceptions import FormException
from db.helper.forms import convert_object_to_id, validate_form_data
from db.models import ProjectType, Topic, Keyword, ProjectPosting, ProfileType


class ProjectPostingFormStep1(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=300, required=True)
    additional_information = forms.CharField(max_length=1000, required=False)
    project_type = forms.ModelChoiceField(queryset=ProjectType.objects.all(), required=True)
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=True)
    keywords = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all(), required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['project_type'] = convert_object_to_id(data.get('project_type', None))
        data['topic'] = convert_object_to_id(data.get('topic', None))
        super().__init__(data=data, **kwargs)


def process_project_posting_form_step_1(user, data):
    errors = {}

    validate_form_data(data)

    form = ProjectPostingFormStep1(data)
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
    project_posting_id = data.get('id', None)
    if project_posting_id is not None:
        project_posting = get_object_or_404(ProjectPosting, pk=project_posting_id)
    else:
        project_posting = ProjectPosting()

    project_posting.title = cleaned_data.get('title')
    project_posting.description = cleaned_data.get('description')
    project_posting.additional_information = cleaned_data.get('additional_information')
    project_posting.project_type = cleaned_data.get('project_type')
    project_posting.topic = cleaned_data.get('topic')
    project_posting.company = cleaned_data.get('company')
    project_posting.student = cleaned_data.get('student')
    project_posting.employee = cleaned_data.get('employee')
    project_posting.save()
    project_posting.keywords.set(cleaned_data.get('keywords'))

    project_posting.slug = f'{slugify(project_posting.title)}-{str(project_posting.id)}'
    project_posting.save()
    return project_posting
