import pytest

from django.contrib.auth.models import AnonymousUser

from db.models import JobPosting, Match

# pylint: disable=R0913


@pytest.mark.django_db
def test_delete_job_posting_as_rightfull_employee(delete_job_posting,
                                                  job_posting_object: JobPosting, company_object,
                                                  user_employee):
    job_posting_object.company = company_object
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    data, errors = delete_job_posting(user_employee, job_posting_object.id)

    assert errors is None
    assert data is not None

    assert data.get('deleteJobPosting').get('success')
    assert not JobPosting.objects.filter(pk=job_posting_object.id).exists()


@pytest.mark.django_db
def test_delete_job_posting_as_wrong_employee(delete_job_posting, job_posting_object: JobPosting,
                                              company_object, user_employee, user_employee_2):
    job_posting_object.company = company_object
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    data, errors = delete_job_posting(user_employee_2, job_posting_object.id)
    assert errors is None
    assert data is not None

    assert data.get('deleteJobPosting') is not None
    assert not data.get('deleteJobPosting').get('success')
    error_message = data.get('deleteJobPosting').get('errors').get('id')[0].get('message')
    assert error_message == 'The job posting is not part of the same company'


@pytest.mark.django_db
def test_delete_job_posting_as_student(delete_job_posting, job_posting_object: JobPosting,
                                       company_object, user_employee, user_student):
    job_posting_object.company = company_object
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    data, errors = delete_job_posting(user_student, job_posting_object.id)
    assert errors is None
    assert data is not None

    assert data.get('deleteJobPosting') is not None
    assert not data.get('deleteJobPosting').get('success')
    error_message = data.get('deleteJobPosting').get('errors').get('company')[0].get('message')
    assert error_message == 'You are not part of a company'


@pytest.mark.django_db
def test_delete_job_posting_as_anonymous(delete_job_posting, job_posting_object: JobPosting):
    data, errors = delete_job_posting(AnonymousUser(), job_posting_object.id)
    assert errors is not None
    assert data is not None

    error = errors[0].get('message')
    node = data.get('node')
    assert node is None
    assert error == "You do not have permission to perform this action"


@pytest.mark.django_db
def test_delete_job_posting_removes_matches(delete_job_posting, job_posting_object: JobPosting,
                                            company_object, user_employee, user_student):
    job_posting_object.company = company_object
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    Match.objects.create(job_posting=job_posting_object,
                         student=user_student.student,
                         initiator=user_employee.type,
                         company_confirmed=True,
                         student_confirmed=True)

    data, errors = delete_job_posting(user_employee, job_posting_object.id)

    assert errors is None
    assert data is not None

    assert data.get('deleteJobPosting').get('success')
    assert not JobPosting.objects.filter(pk=job_posting_object.id).exists()
    matches = Match.objects.all()
    assert len(matches) == 0
