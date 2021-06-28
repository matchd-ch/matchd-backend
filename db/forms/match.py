from datetime import datetime
import pytz

from django.conf import settings
from django.core.exceptions import PermissionDenied

from db.exceptions import FormException
from db.helper import generic_error_dict
from db.helper.forms import validate_company_user_type, validate_form_data, validate_student_user_type
from db.models import Student, Match, JobPosting, ProfileType, ProjectPosting


def get_id_from_data(data, key):
    errors = {}
    if data.get(key) is not None:
        obj_id = data.get(key).get('id')
        if obj_id is not None:
            return obj_id
    errors.update(generic_error_dict(key, 'Select a valid choice', 'invalid'))
    raise FormException(errors=errors)


def send_mails(match_object, created, project=False):
    if project:
        match_object.send_complete_project_match_mail()
    elif created:
        match_object.send_start_job_match_email()
    elif match_object.complete and not match_object.complete_mail_sent:
        match_object.send_complete_job_match_mail()
        match_object.complete_mail_sent = True
        match_object.save()


def process_student_match(user, data):
    errors = {}

    validate_company_user_type(user)
    validate_form_data(data)

    student = None
    job_posting = None
    try:
        student_id = get_id_from_data(data, 'student')
        student = Student.objects.get(pk=student_id)
        job_posting_id = get_id_from_data(data, 'job_posting')
        job_posting = JobPosting.objects.get(pk=job_posting_id)
    except Student.DoesNotExist:
        errors.update(generic_error_dict('student', 'Select a valid choice', 'invalid'))
    except JobPosting.DoesNotExist:
        errors.update(generic_error_dict('job_posting', 'Select a valid choice', 'invalid'))
    except FormException as exception:
        # pylint: disable=W0707
        raise FormException(errors=exception.errors)

    if errors:
        raise FormException(errors=errors)

    match_obj, created = Match.objects.get_or_create(student=student, job_posting=job_posting)
    match_obj.company_confirmed = True
    if created:
        match_obj.initiator = ProfileType.COMPANY
    if not created and not match_obj.complete and match_obj.initiator != ProfileType.COMPANY:
        match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    match_obj.save()

    send_mails(match_obj, created)

    return match_obj


def process_job_posting_match(user, data):
    errors = {}

    validate_student_user_type(user)
    validate_form_data(data)

    job_posting = None
    try:
        job_posting_id = get_id_from_data(data, 'job_posting')
        job_posting = JobPosting.objects.get(pk=job_posting_id)
    except JobPosting.DoesNotExist:
        errors.update(generic_error_dict('job_posting', 'Select a valid choice', 'invalid'))
    except FormException as exception:
        # pylint: disable=W0707
        raise FormException(errors=exception.errors)

    if errors:
        raise FormException(errors=errors)

    match_obj, created = Match.objects.get_or_create(student=user.student, job_posting=job_posting)
    match_obj.student_confirmed = True
    if created:
        match_obj.initiator = ProfileType.STUDENT
    if not created and not match_obj.complete and match_obj.initiator != ProfileType.STUDENT:
        match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    match_obj.save()

    send_mails(match_obj, created)

    return match_obj


def process_project_posting_match(user, data):
    errors = {}

    validate_form_data(data)

    project_posting = None
    try:
        project_posting_id = get_id_from_data(data, 'project_posting')
        project_posting = ProjectPosting.objects.get(pk=project_posting_id)
    except ProjectPosting.DoesNotExist:
        errors.update(generic_error_dict('project_posting', 'Select a valid choice', 'invalid'))
    except FormException as exception:
        # pylint: disable=W0707
        raise FormException(errors=exception.errors)

    if errors:
        raise FormException(errors=errors)

    # pylint: disable=W0612
    match_obj, created = None, None
    if user.type in ProfileType.valid_student_types():
        # do not allow students to match projects of other students
        if project_posting.student is not None:
            raise PermissionDenied('You are not allowed to perform this action.')
        match_obj, created = Match.objects.get_or_create(project_posting=project_posting, student=user.student)
    if user.type in ProfileType.valid_company_types():
        # do not allow companies to match projects of other companies
        if project_posting.company is not None:
            raise PermissionDenied('You are not allowed to perform this action.')
        match_obj, created = Match.objects.get_or_create(project_posting=project_posting, company=user.company)

    match_obj.student_confirmed = True
    match_obj.company_confirmed = True
    match_obj.initiator = user.type
    match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    match_obj.save()

    send_mails(match_obj, created, True)

    return match_obj
