import datetime
from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper.forms import validate_form_data, convert_object_to_id, generic_error_dict, validate_project_posting_step
from db.models import ProjectPosting, ProjectPostingState, Employee, ProfileType
# pylint: disable=R0912
# pylint: disable=R0915


class ProjectPostingAllocationForm(forms.Form):
    state = forms.ChoiceField(choices=ProjectPostingState.choices)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['employee'] = convert_object_to_id(data.get('employee', None))
        super().__init__(data=data, **kwargs)


def process_project_posting_allocation_form(user, data):
    errors = {}

    # validate step and data
    validate_form_data(data)
    project_posting = get_object_or_404(ProjectPosting, id=data.get('id'))
    was_published = project_posting.state == ProjectPostingState.PUBLIC
    validate_project_posting_step(project_posting, 3)

    # do not disable enum conversion as described here:
    # https://docs.graphene-python.org/projects/django/en/latest/queries/#choices-to-enum-conversion
    # otherwise the frontend application will not have an enum type for the state field
    # force lower case of the input (eg. "DRAFT", etc)
    data['state'] = data.get('state').lower()

    form = ProjectPostingAllocationForm(data)
    form.full_clean()
    if form.is_valid():
        # update job posting
        cleaned_data = form.cleaned_data
        project_posting.state = cleaned_data.get('state')
        employee = cleaned_data.get('employee', None)

        # check if employee belongs to the same company as the current user
        if employee is not None:
            if user.type in ProfileType.valid_company_types(
            ) and employee.user.company != user.company:
                errors.update(
                    generic_error_dict('employee', _('Employee does not belong to your company'),
                                       'invalid'))
                raise FormException(errors=errors)

        # check if the project posting belongs to the company
        # ! if the user is a student, both values will be None
        # ! see next if statement
        if user.company != project_posting.company:
            errors.update(
                generic_error_dict('employee',
                                   _('Project posting does not belong to your company.'),
                                   'invalid'))
            raise FormException(errors=errors)

        # check if the project posting belongs to the student
        if user.type in ProfileType.valid_student_types(
        ) and user.student != project_posting.student:
            errors.update(
                generic_error_dict('student', _('Project posting does not belong to you.'),
                                   'invalid'))
            raise FormException(errors=errors)
        project_posting.employee = employee
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    if user.type in ProfileType.valid_company_types():
        user_company = user.company.id
        project_posting_company = project_posting.company.id
        if user_company != project_posting_company:
            errors.update(
                generic_error_dict('employee', _('Project posting does not belong to your company'),
                                   'invalid'))
            raise FormException(errors=errors)
        project_posting.student = None
    elif user.type in ProfileType.valid_student_types():
        if user.student != project_posting.student:
            errors.update(
                generic_error_dict('student', _('Project posting does not belong to you.'),
                                   'invalid'))
            raise FormException(errors=errors)
        project_posting.company = None
        project_posting.employee = None

    # update job posting
    if project_posting.form_step == 3:
        project_posting.form_step = 4

    if not was_published:
        if project_posting.state == ProjectPostingState.PUBLIC:
            project_posting.date_published = datetime.datetime.now()
    else:
        if project_posting.state == ProjectPostingState.DRAFT:
            project_posting.date_published = None

    project_posting.save()

    return project_posting
