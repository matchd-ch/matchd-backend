from django import forms
from django.shortcuts import get_object_or_404

from db.exceptions import FormException
from db.helper.forms import validate_form_data, convert_date
from db.models import ProjectPosting, ProfileType


class ProjectPostingFormStep2(forms.Form):
    project_from_date = forms.DateField(required=False)
    website = forms.URLField(required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['project_from_date'] = convert_date(data.get('project_from_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)


def process_project_posting_form_step_2(user, data):
    errors = {}

    validate_form_data(data)

    form = ProjectPostingFormStep2(data)
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

    project_posting.project_from_date = cleaned_data.get('project_from_date')
    project_posting.website = cleaned_data.get('website')
    # update job posting
    if project_posting.form_step == 2:
        project_posting.form_step = 3

    project_posting.save()
    return project_posting
