import pytest

from db.models import Match

# pylint: disable=R0913


@pytest.mark.django_db
def test_dashboard(login, query_dashboard, user_employee, user_student, job_posting_objects,
                   company_project_posting_objects, student_project_posting_objects):

    for job_posting_object in job_posting_objects:
        job_posting_object.company = user_employee.company
        job_posting_object.employee = user_employee.employee
        job_posting_object.save()

    for project_posting_object in company_project_posting_objects:
        project_posting_object.company = user_employee.company
        project_posting_object.employee = user_employee.employee
        project_posting_object.save()

    Match.objects.create(job_posting=job_posting_objects[0], student=user_student.student, company_confirmed=True,
                         initiator=user_employee.type)
    Match.objects.create(job_posting=job_posting_objects[1], student=user_student.student, student_confirmed=True,
                         initiator=user_student.type)
    Match.objects.create(job_posting=job_posting_objects[2], student=user_student.student, student_confirmed=True,
                         company_confirmed=True, initiator=user_employee.type)

    login(user_employee)
    data, errors = query_dashboard(user_employee)

    assert data is not None
    assert errors is None

    dashboard = data.get('dashboard')
    job_postings = dashboard.get('jobPostings')
    assert len(job_postings) == 3

    latest_job_postings = dashboard.get('latestJobPostings')
    assert latest_job_postings is None

    project_postings = dashboard.get('projectPostings')
    assert len(project_postings) == 3

    latest_project_postings = dashboard.get('latestProjectPostings')
    assert len(latest_project_postings) == len(student_project_posting_objects) - 1  # 2x public, 1x draft

    requested_matches = dashboard.get('requestedMatches')
    assert requested_matches is not None
    assert len(requested_matches) == 1
    assert int(requested_matches[0].get('jobPosting').get('id')) == job_posting_objects[0].id

    unconfirmed_matches = dashboard.get('unconfirmedMatches')
    assert unconfirmed_matches is not None
    assert len(unconfirmed_matches) == 1
    assert int(unconfirmed_matches[0].get('jobPosting').get('id')) == job_posting_objects[1].id

    confirmed_matches = dashboard.get('confirmedMatches')
    assert confirmed_matches is not None
    assert len(confirmed_matches) == 1
    assert int(confirmed_matches[0].get('jobPosting').get('id')) == job_posting_objects[2].id
