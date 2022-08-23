from datetime import datetime
import pytz

from django.conf import settings
from django.core.exceptions import PermissionDenied

from db.exceptions import FormException
from db.helper import generic_error_dict
from db.helper.forms import validate_company_user_type, validate_form_data, validate_student_user_type
from db.models import Student, Match, JobPosting, ProfileType, Challenge


def get_id_from_data(data, key):
    errors = {}
    if data.get(key) is not None:
        obj_id = data.get(key).get('id')
        if obj_id is not None:
            return obj_id
    errors.update(generic_error_dict(key, 'Select a valid choice', 'invalid'))
    raise FormException(errors=errors)


def send_job_posting_mails(match_object, created, user, context):
    if created:
        match_object.send_start_job_match_email(user, context)
    elif match_object.complete and not match_object.complete_mail_sent:
        match_object.send_complete_job_match_mail(user, context)
        match_object.complete_mail_sent = True
        match_object.save()


def send_challenge_mails(match_object, user, context):
    match_object.send_complete_challenge_match_mail(user, context)


def process_student_match(user, data, context):
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
        match_obj.initiator = user.type
    if not created and not match_obj.complete and match_obj.initiator != user.type:
        match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    match_obj.save()

    send_job_posting_mails(match_obj, created, user, context)

    return match_obj


def process_job_posting_match(user, data, context):
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
        match_obj.initiator = user.type
    if not created and not match_obj.complete and match_obj.initiator != user.type:
        match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    match_obj.save()

    send_job_posting_mails(match_obj, created, user, context)

    return match_obj


def process_challenge_match(user, data, context):
    errors = {}

    validate_form_data(data)

    challenge = None
    try:
        challenge_id = get_id_from_data(data, 'challenge')
        challenge = Challenge.objects.get(pk=challenge_id)
    except Challenge.DoesNotExist:
        errors.update(generic_error_dict('challenge', 'Select a valid choice', 'invalid'))
    except FormException as exception:
        # pylint: disable=W0707
        raise FormException(errors=exception.errors)

    if errors:
        raise FormException(errors=errors)

    # pylint: disable=W0612
    match_obj, created = None, None
    if user.type in ProfileType.valid_student_types():
        # do not allow students to match challenges of other students
        if challenge.student is not None:
            raise PermissionDenied('You are not allowed to perform this action.')
        match_obj, created = Match.objects.get_or_create(challenge=challenge, student=user.student)
    if user.type in ProfileType.valid_company_types():
        # do not allow companies to match challenges of other companies
        if challenge.company is not None:
            raise PermissionDenied('You are not allowed to perform this action.')
        match_obj, created = Match.objects.get_or_create(challenge=challenge, company=user.company)

    match_obj.student_confirmed = True
    match_obj.company_confirmed = True
    match_obj.initiator = user.type
    match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    match_obj.save()

    send_challenge_mails(match_obj, user, context)

    return match_obj
