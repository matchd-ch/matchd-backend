from datetime import datetime
import pytz

from django.conf import settings

from db.exceptions import FormException
from db.helper import generic_error_dict
from db.helper.forms import validate_company_user_type, validate_form_data, validate_student_user_type
from db.models import Student, Match, JobPosting, ProfileType


def get_id_from_data(data, key):
    errors = {}
    if data.get(key) is not None:
        obj_id = data.get(key).get('id')
        if obj_id is not None:
            return obj_id
    errors.update(generic_error_dict(key, 'Select a valid choice', 'invalid'))
    raise FormException(errors=errors)


def send_mails(match_object, created):
    if created:
        match_object.send_start_match_email()
    elif match_object.complete and not match_object.complete_mail_sent:
        match_object.send_complete_match_mail()
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
        match_obj.complete = True
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
        match_obj.complete = True
    match_obj.save()

    send_mails(match_obj, created)

    return match_obj
