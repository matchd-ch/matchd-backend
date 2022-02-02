from io import StringIO

import pytest

from django.core import management

from db.models import JobPostingState, ProfileState, JobPostingLanguageRelation, UserLanguageRelation, Match


# pylint: disable=R0913
# pylint: disable=R0915
@pytest.mark.django_db
def test_student_matching(job_posting_object, skill_objects, branch_objects,
                          job_type_objects_date_range, user_employee, soft_skill_objects,
                          cultural_fit_objects, user_student, user_student_2, student_matching,
                          login, language_objects, language_level_objects, student_fallback_images):

    branch = branch_objects[0]
    job_type = job_type_objects_date_range[0]
    language = language_objects[0]
    language_level = language_level_objects[0]

    user_employee.company.street = 'street'
    user_employee.company.zip = '1337'
    user_employee.company.city = 'nowhere'
    user_employee.company.save()
    user_employee.company.soft_skills.set(soft_skill_objects[:6])
    user_employee.company.cultural_fits.set(cultural_fit_objects[:6])
    user_employee.company.save()

    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.job_type = job_type
    job_posting_object.workload = 100
    job_posting_object.company = user_employee.company
    job_posting_object.job_from_date = '2021-08-01'
    job_posting_object.job_to_date = '2022-07-31'
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()
    job_posting_object.skills.set(skill_objects[:2])
    job_posting_object.save()
    job_posting_object.branches.set([branch])

    JobPostingLanguageRelation.objects.create(language=language,
                                              language_level=language_level,
                                              job_posting=job_posting_object)

    # a 100% match
    user_student.student.branch = job_posting_object.branches.all()[0]
    user_student.student.job_type = job_posting_object.job_type
    user_student.student.job_from_date = job_posting_object.job_from_date
    user_student.student.job_to_date = job_posting_object.job_to_date
    user_student.student.state = ProfileState.PUBLIC
    user_student.student.save()
    user_student.student.skills.set(skill_objects[:2])
    user_student.student.soft_skills.set(soft_skill_objects[:6])
    user_student.student.cultural_fits.set(cultural_fit_objects[:6])
    user_student.student.save()

    UserLanguageRelation.objects.create(language=language,
                                        language_level=language_level,
                                        student=user_student.student)

    # a bad match
    user_student_2.student.branch = job_posting_object.branches.all()[0]
    user_student_2.student.job_type = job_type_objects_date_range[1]
    user_student_2.student.job_from_date = '2022-08-01'
    user_student_2.student.job_to_date = '2023-07-31'
    user_student_2.student.state = ProfileState.PUBLIC
    user_student_2.student.save()
    user_student_2.student.skills.set(skill_objects[-2:])
    user_student_2.student.soft_skills.set(soft_skill_objects[-6:])
    user_student_2.student.cultural_fits.set(cultural_fit_objects[-6:])
    user_student_2.student.save()

    UserLanguageRelation.objects.create(language=language_objects[1],
                                        language_level=language_level_objects[1],
                                        student=user_student_2.student)

    management.call_command('update_index', stdout=StringIO())

    Match.objects.create(student=user_student.student,
                         job_posting=job_posting_object,
                         initiator=user_employee.type,
                         company_confirmed=True)

    login(user_employee)
    data, errors = student_matching(user_employee, job_posting_object)
    assert data is not None
    assert errors is None

    matches = data.get('matches')
    assert matches is not None
    assert len(matches) == 2

    # max score for job posting is: 20 (see db/search/calculators/student.py)
    # user_student is a perfect match --> score = 19
    # user_student matches only with branch --> score = 0
    best_match = matches[0]
    assert int(best_match.get('id')) == user_student.student.id
    assert float(best_match.get('score')) == 1
    assert float(best_match.get('rawScore')) == 1
    match_status = best_match.get('matchStatus')
    assert match_status is not None
    assert match_status.get('confirmed') is False
    assert match_status.get('initiator') == user_employee.type.upper()

    worst_match = matches[1]
    assert int(worst_match.get('id')) == user_student_2.student.id
    assert float(worst_match.get('score')) == 0
    assert float(worst_match.get('rawScore')) == 0
    match_status = worst_match.get('matchStatus')
    assert match_status is None
