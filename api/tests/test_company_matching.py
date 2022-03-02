from io import StringIO

import pytest

from django.core import management

from graphql_relay import to_global_id

from db.helper.forms import convert_date
from db.models import ProfileState, Match, JobPostingState


# pylint: disable=R0913
# pylint: disable=R0915
@pytest.mark.django_db
def test_match_company(user_student, company_matching, soft_skill_objects, cultural_fit_objects,
                       user_employee, user_employee_2, branch_objects, job_posting_object,
                       company_fallback_images):
    user_student.student.branch = branch_objects[0]
    user_student.student.job_from_date = convert_date('2021-08-01', '%Y-%m-%d')
    user_student.student.job_to_date = convert_date('2022-07-31', '%Y-%m-%d')
    user_student.student.save()
    user_student.student.soft_skills.set(soft_skill_objects[:6])
    user_student.student.cultural_fits.set(cultural_fit_objects[:6])
    user_student.student.save()

    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.workload = 100
    job_posting_object.company = user_employee.company
    job_posting_object.job_from_date = user_student.student.job_from_date
    job_posting_object.job_to_date = user_student.student.job_to_date
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    # a 100% match
    user_employee.company.branches.set(branch_objects)
    user_employee.company.soft_skills.set(soft_skill_objects[:6])
    user_employee.company.cultural_fits.set(cultural_fit_objects[:6])
    user_employee.company.state = ProfileState.PUBLIC
    user_employee.company.street = 'street'
    user_employee.company.zip = '1337'
    user_employee.company.city = 'nowhere'
    user_employee.company.save()

    # a bad match
    user_employee_2.company.branches.set(branch_objects)
    user_employee_2.company.soft_skills.set(soft_skill_objects[-6:])
    user_employee_2.company.cultural_fits.set(cultural_fit_objects[-6:])
    user_employee_2.company.state = ProfileState.PUBLIC
    user_employee_2.company.street = 'street'
    user_employee_2.company.zip = '1337'
    user_employee_2.company.city = 'nowhere'
    user_employee_2.company.save()

    Match.objects.create(student=user_student.student,
                         job_posting=job_posting_object,
                         initiator=user_student.type,
                         student_confirmed=True)

    management.call_command('update_index', stdout=StringIO())

    data, errors = company_matching(user_student)
    assert errors is None
    assert data is not None

    matches = data.get('matches')
    assert matches is not None
    assert len(matches) == 2

    best_match = matches[0]
    assert best_match.get('id') == to_global_id('Company', user_employee.company.id)
    assert float(best_match.get('score')) == 1
    assert float(best_match.get('rawScore')) == 1

    match_status = best_match.get('matchStatus')
    assert match_status is not None
    assert match_status.get('confirmed') is False
    assert match_status.get('initiator') == user_student.type.upper()

    worst_match = matches[1]
    assert worst_match.get('id') == to_global_id('Company', user_employee_2.company.id)
    assert float(worst_match.get('score')) == 0
    assert float(worst_match.get('rawScore')) == 0

    match_status = worst_match.get('matchStatus')
    assert match_status is None
