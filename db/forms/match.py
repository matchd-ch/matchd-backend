import pytz
from datetime import datetime

from django.conf import settings

from db.exceptions import FormException
from db.helper import generic_error_dict
from db.models import Student, Match, Company
from db.models.match import MatchInitiator


def process_student_match(company, data):
    errors = {}
    student = data.get('student')
    if company is None:
        errors.update(generic_error_dict('student', 'Missing student', 'required'))
    if errors:
        raise FormException(errors=errors)

    student_id = student.get('id')
    match_obj, created = None, None,
    try:
        target = Student.objects.get(pk=student_id)
        match_obj, created = Match.objects.get_or_create(company=company, student=target)
        match_obj.company_confirmed = True
        if match_obj.initiator == MatchInitiator.COMPANY:
            return match_obj
        if created:
            match_obj.initiator = MatchInitiator.COMPANY
    except Student.DoesNotExist:
        errors.update(generic_error_dict('student', 'Select a valid choice', 'invalid'))
    if errors:
        raise FormException(errors=errors)

    if match_obj is None:
        errors.update(generic_error_dict('non_field_error', 'Failed to create match', 'error'))
        raise FormException(errors=errors)

    if not created and not match_obj.complete:
        match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        match_obj.complete = True
    match_obj.save()
    return match_obj


def process_company_match(student, data):
    errors = {}
    company = data.get('company')
    if company is None:
        errors.update(generic_error_dict('company', 'Missing company', 'required'))
    if errors:
        raise FormException(errors=errors)

    company_id = company.get('id')
    match_obj, created = None, None,
    try:
        target = Company.objects.get(pk=company_id)
        match_obj, created = Match.objects.get_or_create(student=student, company=target)
        match_obj.student_confirmed = True
        if match_obj.initiator == MatchInitiator.STUDENT:
            return match_obj
        if created:
            match_obj.initiator = MatchInitiator.STUDENT
    except Company.DoesNotExist:
        errors.update(generic_error_dict('company', 'Select a valid choice', 'invalid'))
    if errors:
        raise FormException(errors=errors)

    if match_obj is None:
        errors.update(generic_error_dict('non_field_error', 'Failed to create match', 'error'))
        raise FormException(errors=errors)

    if not created and not match_obj.complete:
        match_obj.date_confirmed = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        match_obj.complete = True
    match_obj.save()
    return match_obj
