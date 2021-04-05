import pytest
from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import ProfileType, ProfileState, Hobby, OnlineProject

# pylint: disable=C0103
# pylint: disable=R0913
# pylint: disable=R0915


@pytest.mark.django_db
def test_me_student(login, me, user_student, skill_objects, soft_skill_objects, cultural_fit_objects):
    user_student.first_name = 'John'
    user_student.last_name = 'Doe'
    user_student.save()
    user_student.student.profile_step = 3
    user_student.student.state = ProfileState.ANONYMOUS
    user_student.student.mobile = '+41711234567'
    user_student.student.zip = '1337'
    user_student.student.city = 'nowhere'
    user_student.student.street = 'street 1337'
    user_student.student.date_of_birth = convert_date('01.03.1337')
    user_student.student.nickname = 'nickname'
    user_student.student.school_name = 'school name'
    user_student.student.field_of_study = 'field of study'
    user_student.student.graduation = convert_date('03.1337', '%m.%Y')
    user_student.student.distinction = 'distinction'
    user_student.student.skills.set(skill_objects)
    hobbies = [
        Hobby.objects.create(id=1, name='hobby 1', student=user_student.student),
        Hobby.objects.create(id=2, name='hobby 2', student=user_student.student)
    ]
    user_student.student.hobbies.set(hobbies)
    online_projects = [
        OnlineProject.objects.create(id=1, url='http://www.project1.lo', student=user_student.student),
        OnlineProject.objects.create(id=2, url='http://www.project2.lo', student=user_student.student)
    ]
    user_student.student.online_projects.set(online_projects)
    user_student.student.soft_skills.set(soft_skill_objects[:6])
    user_student.student.cultural_fits.set(cultural_fit_objects[:6])
    user_student.student.save()

    login(user_student)
    data, errors = me(user_student)
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
    assert student.get('profileStep') == 3
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineProjects')) == 2
    assert len(student.get('softSkills')) == 6
    assert len(student.get('culturalFits')) == 6

    company = user.get('company')
    assert company is None


@pytest.mark.django_db
def test_me_student_without_login(me):
    data, errors = me(AnonymousUser())
    assert errors is not None
    assert data is not None

    user = data.get('me')
    assert user is None
