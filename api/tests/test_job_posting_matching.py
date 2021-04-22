from io import StringIO

import pytest
from django.core import management

from db.helper.forms import convert_date
from db.models import JobPostingState, ProfileState, JobPostingLanguageRelation, UserLanguageRelation, Match

# pylint: disable=R0913
# pylint: disable=R0915


@pytest.mark.django_db
def test_job_posting_matching(job_posting_object, job_posting_object_2, skill_objects, branch_objects,
                              job_type_objects_date_range, user_employee, soft_skill_objects, cultural_fit_objects,
                              user_student, job_posting_matching, login, language_objects, language_level_objects,
                              user_employee_2):
    branch = branch_objects[0]
    job_type = job_type_objects_date_range[0]
    language = language_objects[0]
    language_level = language_level_objects[0]

    user_student.student.branch = branch
    user_student.student.job_type = job_type
    user_student.student.job_from_date = convert_date('2021-08-01', '%Y-%m-%d')
    user_student.student.job_to_date = convert_date('2022-07-31', '%Y-%m-%d')
    user_student.student.state = ProfileState.PUBLIC
    user_student.student.save()
    user_student.student.skills.set(skill_objects[:2])
    user_student.student.soft_skills.set(soft_skill_objects[:6])
    user_student.student.cultural_fits.set(cultural_fit_objects[:6])
    user_student.student.save()

    UserLanguageRelation.objects.create(language=language, language_level=language_level, student=user_student.student)

    user_employee.company.street = 'street'
    user_employee.company.zip = '1337'
    user_employee.company.city = 'nowhere'
    user_employee.company.save()
    user_employee.company.soft_skills.set(soft_skill_objects[:6])
    user_employee.company.cultural_fits.set(cultural_fit_objects[:6])
    user_employee.company.save()

    # a 100% match
    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.branch = branch
    job_posting_object.job_type = job_type
    job_posting_object.workload = 100
    job_posting_object.company = user_employee.company
    job_posting_object.job_from_date = user_student.student.job_from_date
    job_posting_object.job_to_date = user_student.student.job_to_date
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()
    job_posting_object.skills.set(skill_objects[:2])
    job_posting_object.save()

    JobPostingLanguageRelation.objects.create(language=language, language_level=language_level,
                                              job_posting=job_posting_object)

    user_employee_2.company.street = 'street'
    user_employee_2.company.zip = '1337'
    user_employee_2.company.city = 'nowhere'
    user_employee_2.company.save()
    user_employee_2.company.soft_skills.set(soft_skill_objects[-6:])
    user_employee_2.company.cultural_fits.set(cultural_fit_objects[-6:])
    user_employee_2.company.save()

    # a bad match
    job_posting_object_2.state = JobPostingState.PUBLIC
    job_posting_object_2.title = 'title2'
    job_posting_object_2.slug = 'title2'
    job_posting_object_2.branch = branch
    job_posting_object_2.job_type = job_type_objects_date_range[1]
    job_posting_object_2.workload = 10
    job_posting_object_2.company = user_employee_2.company
    job_posting_object_2.job_from_date = convert_date('2022-08-01', '%Y-%m-%d')
    job_posting_object_2.job_to_date = convert_date('2023-07-31', '%Y-%m-%d')
    job_posting_object_2.employee = user_employee_2.employee
    job_posting_object_2.save()
    job_posting_object_2.skills.set(skill_objects[-2:])
    job_posting_object_2.save()

    JobPostingLanguageRelation.objects.create(language=language_objects[1], language_level=language_level_objects[1],
                                              job_posting=job_posting_object_2)

    management.call_command('update_index', stdout=StringIO())

    Match.objects.create(student=user_student.student, job_posting=job_posting_object, initiator=user_student.type,
                         student_confirmed=True)

    login(user_student)
    data, errors = job_posting_matching(user_student, user_student.student.branch, user_student.student.job_type)
    assert data is not None
    assert errors is None

    matches = data.get('matches')
    assert matches is not None
    assert len(matches) == 2

    # max score for job posting is: 20 (see db/search/calculators/student.py)
    # job_posting_object is a perfect match --> score = 20
    # job_posting_object_2 matches only with branch --> score = 0
    best_match = matches[0]
    assert int(best_match.get('id')) == job_posting_object.id
    assert float(best_match.get('score')) == 1
    assert float(best_match.get('rawScore')) == 1
    match_status = best_match.get('matchStatus')
    assert match_status is not None
    assert match_status.get('confirmed') is False
    assert match_status.get('initiator') == user_student.type.upper()

    worst_match = matches[1]
    assert int(worst_match.get('id')) == job_posting_object_2.id
    assert float(worst_match.get('score')) == 0
    assert float(worst_match.get('rawScore')) == 0
    match_status = worst_match.get('matchStatus')
    assert match_status is None
