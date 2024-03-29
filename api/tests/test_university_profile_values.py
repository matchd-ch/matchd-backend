import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import SoftSkill, CulturalFit, ProfileState


@pytest.mark.django_db
def test_values(login, user_employee, university_values, soft_skill_objects, cultural_fit_objects):
    login(user_employee)
    data, errors = university_values(user_employee, soft_skill_objects[:6],
                                     cultural_fit_objects[:6])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileValues') is not None
    assert data.get('universityProfileValues').get('success')

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.soft_skills.all()) == 6
    assert len(user.company.cultural_fits.all()) == 6
    assert user.company.state == ProfileState.PUBLIC


@pytest.mark.django_db
def test_values_without_login(user_employee, university_values, soft_skill_objects,
                              cultural_fit_objects):
    data, errors = university_values(AnonymousUser(), soft_skill_objects[:6],
                                     cultural_fit_objects[:6])

    assert errors is not None
    assert data is not None
    assert data.get('universityProfileValues') is None

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.soft_skills.all()) == 0
    assert len(user.company.cultural_fits.all()) == 0


@pytest.mark.django_db
def test_values_as_student(login, user_student, university_values, soft_skill_objects,
                           cultural_fit_objects):
    login(user_student)
    data, errors = university_values(user_student, soft_skill_objects[:6], cultural_fit_objects[:6])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileValues') is not None

    errors = data.get('universityProfileValues').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_values_invalid_data(login, user_employee, university_values):
    login(user_employee)
    data, errors = university_values(user_employee, [SoftSkill(id=1337)], [CulturalFit(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileValues') is not None
    assert data.get('universityProfileValues').get('success') is False

    errors = data.get('universityProfileValues').get('errors')
    assert errors is not None
    assert 'softSkills' in errors
    assert 'culturalFits' in errors


@pytest.mark.django_db
def test_values_empty_soft_skills_and_cultural_fits(login, user_employee, university_values):
    login(user_employee)
    data, errors = university_values(user_employee, [], [])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileValues') is not None
    assert data.get('universityProfileValues').get('success') is True

    errors = data.get('universityProfileValues').get('errors')
    assert errors is None


@pytest.mark.django_db
def test_values_too_many_soft_skills_and_cultural_fits(login, user_employee, university_values,
                                                       soft_skill_objects, cultural_fit_objects):
    login(user_employee)
    data, errors = university_values(user_employee, soft_skill_objects[:7],
                                     cultural_fit_objects[:7])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileValues') is not None
    assert data.get('universityProfileValues').get('success') is False

    errors = data.get('universityProfileValues').get('errors')
    assert errors is not None
    assert 'softSkills' in errors
    assert 'culturalFits' in errors
