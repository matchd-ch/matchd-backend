import pytest

from graphql_relay import to_global_id

from db.models import Match

# pylint: disable=R0913


@pytest.mark.django_db
def test_dashboard(login, query_dashboard, user_employee, user_student, job_posting_objects,
                   company_challenge_objects, student_challenge_objects):

    for job_posting_object in job_posting_objects:
        job_posting_object.company = user_employee.company
        job_posting_object.employee = user_employee.employee
        job_posting_object.save()

    for challenge_object in company_challenge_objects:
        challenge_object.company = user_employee.company
        challenge_object.employee = user_employee.employee
        challenge_object.save()

    for challenge_object in student_challenge_objects:
        challenge_object.student = user_student.student
        challenge_object.save()

    # job posting matches
    Match.objects.create(job_posting=job_posting_objects[0],
                         student=user_student.student,
                         company_confirmed=True,
                         initiator=user_employee.type)
    Match.objects.create(job_posting=job_posting_objects[1],
                         student=user_student.student,
                         student_confirmed=True,
                         initiator=user_student.type)
    Match.objects.create(job_posting=job_posting_objects[2],
                         student=user_student.student,
                         student_confirmed=True,
                         company_confirmed=True,
                         initiator=user_employee.type)

    # challenge matches
    Match.objects.create(challenge=company_challenge_objects[0],
                         student=user_student.student,
                         company_confirmed=True,
                         student_confirmed=True,
                         initiator=user_student.type)
    Match.objects.create(challenge=student_challenge_objects[0],
                         company=user_employee.company,
                         company_confirmed=True,
                         student_confirmed=True,
                         initiator=user_employee.type)

    login(user_employee)
    data, errors = query_dashboard(user_employee)

    assert data is not None
    assert errors is None

    dashboard = data.get('dashboard')
    job_postings = dashboard.get('jobPostings')
    assert len(job_postings) == 3

    latest_job_postings = dashboard.get('latestJobPostings')
    assert latest_job_postings is None

    challenges = dashboard.get('challenges')
    assert len(challenges) == len(company_challenge_objects)

    latest_challenges = dashboard.get('latestChallenges')
    assert len(latest_challenges) == len(student_challenge_objects) - 1    # 2x public, 1x draft

    requested_matches = dashboard.get('requestedMatches')
    assert requested_matches is not None
    assert len(requested_matches) == 1
    assert requested_matches[0].get('jobPosting').get('id') == to_global_id(
        'JobPosting', job_posting_objects[0].id)

    unconfirmed_matches = dashboard.get('unconfirmedMatches')
    assert unconfirmed_matches is not None
    assert len(unconfirmed_matches) == 1
    assert unconfirmed_matches[0].get('jobPosting').get('id') == to_global_id(
        'JobPosting', job_posting_objects[1].id)

    confirmed_matches = dashboard.get('confirmedMatches')
    assert confirmed_matches is not None
    assert len(confirmed_matches) == 1
    assert confirmed_matches[0].get('jobPosting').get('id') == to_global_id(
        'JobPosting', job_posting_objects[2].id)

    challenge_matches = dashboard.get('challengeMatches')
    assert challenge_matches is not None
    assert len(challenge_matches) == 2
    assert challenge_matches[0].get('challenge').get('id') == to_global_id(
        'Challenge', company_challenge_objects[0].id)
    assert challenge_matches[1].get('challenge').get('id') == to_global_id(
        'Challenge', student_challenge_objects[0].id)
