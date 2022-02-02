import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import SoftSkill, CulturalFit, ProfileState


@pytest.mark.django_db
def test_step_4(login, user_employee, university_step_4, soft_skill_objects, cultural_fit_objects):
    user_employee.company.profile_step = 4
    user_employee.company.save()
    login(user_employee)
    data, errors = university_step_4(user_employee, soft_skill_objects[:6],
                                     cultural_fit_objects[:6])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep4') is not None
    assert data.get('universityProfileStep4').get('success')

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.soft_skills.all()) == 6
    assert len(user.company.cultural_fits.all()) == 6
    assert user.company.profile_step == 5
    assert user.company.state == ProfileState.PUBLIC


@pytest.mark.django_db
def test_step_4_without_login(user_employee, university_step_4, soft_skill_objects,
                              cultural_fit_objects):
    data, errors = university_step_4(AnonymousUser(), soft_skill_objects[:6],
                                     cultural_fit_objects[:6])

    assert errors is not None
    assert data is not None
    assert data.get('universityProfileStep4') is None

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.soft_skills.all()) == 0
    assert len(user.company.cultural_fits.all()) == 0
    assert user.company.profile_step == 1


@pytest.mark.django_db
def test_step_4_as_student(login, user_student, university_step_4, soft_skill_objects,
                           cultural_fit_objects):
    login(user_student)
    data, errors = university_step_4(user_student, soft_skill_objects[:6], cultural_fit_objects[:6])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep4') is not None

    errors = data.get('universityProfileStep4').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_4_invalid_step(login, user_employee, university_step_4, soft_skill_objects,
                             cultural_fit_objects):
    user_employee.company.profile_step = 0
    user_employee.company.save()
    login(user_employee)
    data, errors = university_step_4(user_employee, soft_skill_objects[:6],
                                     cultural_fit_objects[:6])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep4') is not None
    assert data.get('universityProfileStep4').get('success') is False

    errors = data.get('universityProfileStep4').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 0


@pytest.mark.django_db
def test_step_4_invalid_data(login, user_employee, university_step_4):
    user_employee.company.profile_step = 4
    user_employee.company.save()
    login(user_employee)
    data, errors = university_step_4(user_employee, [SoftSkill(id=1337)], [CulturalFit(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep4') is not None
    assert data.get('universityProfileStep4').get('success') is False

    errors = data.get('universityProfileStep4').get('errors')
    assert errors is not None
    assert 'softSkills' in errors
    assert 'culturalFits' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 4


@pytest.mark.django_db
def test_step_4_too_few_soft_skills_and_cultural_fits(login, user_employee, university_step_4,
                                                      soft_skill_objects, cultural_fit_objects):
    user_employee.company.profile_step = 4
    user_employee.company.save()
    login(user_employee)
    data, errors = university_step_4(user_employee, soft_skill_objects[:5],
                                     cultural_fit_objects[:5])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep4') is not None
    assert data.get('universityProfileStep4').get('success') is False

    errors = data.get('universityProfileStep4').get('errors')
    assert errors is not None
    assert 'softSkills' in errors
    assert 'culturalFits' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 4


@pytest.mark.django_db
def test_step_4_too_many_soft_skills_and_cultural_fits(login, user_employee, university_step_4,
                                                       soft_skill_objects, cultural_fit_objects):
    user_employee.company.profile_step = 4
    user_employee.company.save()
    login(user_employee)
    data, errors = university_step_4(user_employee, soft_skill_objects[:7],
                                     cultural_fit_objects[:7])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep4') is not None
    assert data.get('universityProfileStep4').get('success') is False

    errors = data.get('universityProfileStep4').get('errors')
    assert errors is not None
    assert 'softSkills' in errors
    assert 'culturalFits' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 4
