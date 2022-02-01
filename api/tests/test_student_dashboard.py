import pytest

from graphql_relay import to_global_id

from db.models import Match, JobPostingState


# pylint: disable=R0913
@pytest.mark.django_db
def test_dashboard(login, query_dashboard, user_employee, user_student, job_posting_objects, branch_objects,
                   student_project_posting_objects, company_project_posting_objects):

    user_student.student.branch = branch_objects[0]
    user_student.student.save()

    for job_posting_object in job_posting_objects:
        job_posting_object.company = user_employee.company
        job_posting_object.employee = user_employee.employee
        job_posting_object.state = JobPostingState.PUBLIC
        job_posting_object.save()
        job_posting_object.branches.set([branch_objects[0]])

    for project_posting_object in company_project_posting_objects:
        project_posting_object.company = user_employee.company
        project_posting_object.employee = user_employee.employee
        project_posting_object.save()

    for project_posting_object in student_project_posting_objects:
        project_posting_object.student = user_student.student
        project_posting_object.save()

    # job posting matches
    Match.objects.create(job_posting=job_posting_objects[0], student=user_student.student, company_confirmed=True,
                         initiator=user_employee.type)
    Match.objects.create(job_posting=job_posting_objects[1], student=user_student.student, student_confirmed=True,
                         initiator=user_student.type)
    Match.objects.create(job_posting=job_posting_objects[2], student=user_student.student, student_confirmed=True,
                         company_confirmed=True, initiator=user_employee.type)

    # project posting matches
    Match.objects.create(project_posting=company_project_posting_objects[0], student=user_student.student,
                         company_confirmed=True, student_confirmed=True, initiator=user_student.type)
    Match.objects.create(project_posting=student_project_posting_objects[0], company=user_employee.company,
                         company_confirmed=True, student_confirmed=True, initiator=user_employee.type)

    login(user_student)
    data, errors = query_dashboard(user_student)

    assert data is not None
    assert errors is None

    dashboard = data.get('dashboard')

    job_postings = dashboard.get('jobPostings')
    assert job_postings is None

    latest_job_postings = dashboard.get('latestJobPostings')
    assert len(latest_job_postings) == 3

    project_postings = dashboard.get('projectPostings')
    assert len(project_postings) == 3

    latest_project_postings = dashboard.get('latestProjectPostings')
    assert len(latest_project_postings) == len(company_project_posting_objects) - 1  # 2x public, 1x draft

    requested_matches = dashboard.get('requestedMatches')
    assert requested_matches is not None
    assert len(requested_matches) == 1
    assert requested_matches[0].get('jobPosting').get('id') == to_global_id(
        'JobPosting', job_posting_objects[1].id
    )

    unconfirmed_matches = dashboard.get('unconfirmedMatches')
    assert unconfirmed_matches is not None
    assert len(unconfirmed_matches) == 1
    assert unconfirmed_matches[0].get('jobPosting').get('id') == to_global_id(
        'JobPosting', job_posting_objects[0].id
    )

    confirmed_matches = dashboard.get('confirmedMatches')
    assert confirmed_matches is not None
    assert len(confirmed_matches) == 1
    assert confirmed_matches[0].get('jobPosting').get('id') == to_global_id(
        'JobPosting', job_posting_objects[2].id
    )

    project_matches = dashboard.get('projectMatches')
    assert project_matches is not None
    assert len(project_matches) == 2
    assert project_matches[0].get('projectPosting').get('id') == to_global_id(
        'ProjectPosting', company_project_posting_objects[0].id
    )
    assert project_matches[1].get('projectPosting').get('id') == to_global_id(
        'ProjectPosting', student_project_posting_objects[0].id
    )
