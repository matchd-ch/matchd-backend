from datetime import datetime
import pytz

from django.conf import settings

from db.exceptions import FormException
from db.helper import generic_error_dict
from db.models import Student, Match, Company, JobPosting
from db.models.match import MatchInitiator


# pylint: disable=R0912
def process_student_match(company, data):
    errors = {}
    student = data.get('student')
    job_posting = data.get('job_posting')
    if company is None:
        if job_posting is None:
            errors.update(generic_error_dict('non_field_errors', 'Missing company or job posting', 'required'))
    if errors:
        raise FormException(errors=errors)

    if job_posting is not None:
        job_posting_id = job_posting.get('id')
        if job_posting_id is not None:
            try:
                job_posting = JobPosting.objects.get(pk=job_posting_id)
            except JobPosting.DoesNotExist:
                errors.update(generic_error_dict('job_posting', 'Select a valid choice', 'invalid'))
    if errors:
        raise FormException(errors=errors)

    if job_posting is not None and company != job_posting.company:
        errors.update(generic_error_dict('company', 'Job Posting does not belong to this company', 'invalid'))
        raise FormException(errors=errors)

    student_id = student.get('id')
    match_obj, created = None, None
    try:
        target = Student.objects.get(pk=student_id)
        match_obj, created = Match.objects.get_or_create(company=company, student=target, job_posting=job_posting)
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


def process_company_or_job_posting_match(student, data):
    errors = {}
    job_posting = data.get('job_posting')
    company = data.get('company')
    if job_posting is None:
        if company is None:
            errors.update(generic_error_dict('non_field_errors', 'Missing company or job posting', 'required'))
    if errors:
        raise FormException(errors=errors)

    if job_posting is not None:
        job_posting_id = job_posting.get('id')
        if job_posting_id is not None:
            try:
                job_posting = JobPosting.objects.get(pk=job_posting_id)
            except JobPosting.DoesNotExist:
                errors.update(generic_error_dict('job_posting', 'Select a valid choice', 'invalid'))

    if company is not None:
        company_id = company.get('id')
        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            errors.update(generic_error_dict('company', 'Select a valid choice', 'invalid'))

    if errors:
        raise FormException(errors=errors)

    if company is not None and job_posting is not None and company != job_posting.company:
        errors.update(generic_error_dict('company', 'Job Posting does not belong to this company', 'invalid'))
        raise FormException(errors=errors)

    if job_posting is not None:
        company = job_posting.company

    match_obj, created = None, None
    try:
        match_obj, created = Match.objects.get_or_create(student=student, company=company, job_posting=job_posting)
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
