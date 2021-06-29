import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileType, ProfileState

# pylint: disable=C0103
# pylint: disable=R0913
# pylint: disable=R0915


@pytest.mark.django_db
def test_me_student(login, me, user_student_full_profile, skill_objects, branch_objects, job_type_objects,
                    student_project_posting_objects):

    for project_posting in student_project_posting_objects:
        project_posting.student = user_student_full_profile.student
        project_posting.save()

    login(user_student_full_profile)
    data, errors = me(user_student_full_profile)
    assert errors is None
    assert data is not None

    user = data.get('me')
    assert user is not None
    assert user.get('username') == 'student@matchd.test'
    assert user.get('email') == 'student@matchd.test'
    assert user.get('firstName') == 'John'
    assert user.get('lastName') == 'Doe'
    assert user.get('type') == ProfileType.STUDENT.upper()

    student = user.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('profileStep') == 3
    assert int(student.get('branch').get('id')) == branch_objects[0].id
    assert int(student.get('jobType').get('id')) == job_type_objects[0].id
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineProjects')) == 2
    assert len(student.get('softSkills')) == 6
    assert len(student.get('culturalFits')) == 6
    assert len(student.get('projectPostings')) == 3  # public + draft

    company = user.get('company')
    assert company is None


@pytest.mark.django_db
def test_me_student_without_login(me):
    data, errors = me(AnonymousUser())
    assert errors is not None
    assert data is not None

    user = data.get('me')
    assert user is None
