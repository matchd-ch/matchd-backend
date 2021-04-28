import pytest

from db.models import Match, JobPostingState


# pylint: disable=R0913
@pytest.mark.django_db
def test_dashboard(login, query_dashboard, user_employee, user_student, job_posting_objects, branch_objects):

    user_student.student.branch = branch_objects[0]
    user_student.student.save()

    for job_posting_object in job_posting_objects:
        job_posting_object.company = user_employee.company
        job_posting_object.employee = user_employee.employee
        job_posting_object.branch = branch_objects[0]
        job_posting_object.state = JobPostingState.PUBLIC
        job_posting_object.save()

    Match.objects.create(job_posting=job_posting_objects[0], student=user_student.student, company_confirmed=True,
                         initiator=user_employee.type)
    Match.objects.create(job_posting=job_posting_objects[1], student=user_student.student, student_confirmed=True,
                         initiator=user_student.type)
    Match.objects.create(job_posting=job_posting_objects[2], student=user_student.student, student_confirmed=True,
                         company_confirmed=True, initiator=user_employee.type)

    login(user_student)
    data, errors = query_dashboard(user_student)

    assert data is not None
    assert errors is None

    dashboard = data.get('dashboard')
    job_postings = dashboard.get('jobPostings')
    assert len(job_postings) == 3

    requested_matches = dashboard.get('requestedMatches')
    assert requested_matches is not None
    assert len(requested_matches) == 1
    assert int(requested_matches[0].get('jobPosting').get('id')) == job_posting_objects[1].id

    unconfirmed_matches = dashboard.get('unconfirmedMatches')
    assert unconfirmed_matches is not None
    assert len(unconfirmed_matches) == 1
    assert int(unconfirmed_matches[0].get('jobPosting').get('id')) == job_posting_objects[0].id

    confirmed_matches = dashboard.get('confirmedMatches')
    assert confirmed_matches is not None
    assert len(confirmed_matches) == 1
    assert int(confirmed_matches[0].get('jobPosting').get('id')) == job_posting_objects[2].id
