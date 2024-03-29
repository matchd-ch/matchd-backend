import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import SoftSkill, CulturalFit


@pytest.mark.django_db
def test_character(login, user_student, student_character, soft_skill_objects,
                   cultural_fit_objects):
    login(user_student)
    data, errors = student_character(user_student, soft_skill_objects[:6], cultural_fit_objects[:6])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileCharacter') is not None
    assert data.get('studentProfileCharacter').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    soft_skills = user.student.soft_skills.all()
    for obj in soft_skill_objects[:6]:
        assert obj in soft_skills
    cultural_fits = user.student.cultural_fits.all()
    for obj in cultural_fit_objects[:6]:
        assert obj in cultural_fits


@pytest.mark.django_db
def test_character_without_login(user_student, student_character, soft_skill_objects,
                                 cultural_fit_objects):
    data, errors = student_character(AnonymousUser(), soft_skill_objects[:6],
                                     cultural_fit_objects[:6])
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileCharacter') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert len(user.student.soft_skills.all()) == 0
    assert len(user.student.cultural_fits.all()) == 0


@pytest.mark.django_db
def test_character_as_company(login, user_employee, student_character, soft_skill_objects,
                              cultural_fit_objects):
    login(user_employee)
    data, errors = student_character(user_employee, soft_skill_objects[:6],
                                     cultural_fit_objects[:6])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileCharacter') is not None

    errors = data.get('studentProfileCharacter').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_character_with_invalid_data(login, user_student, student_character, soft_skill_objects,
                                     cultural_fit_objects):
    login(user_student)
    data, errors = student_character(user_student, soft_skill_objects[:5] + [SoftSkill(id=1337)],
                                     cultural_fit_objects[:5] + [CulturalFit(id=1337)])

    assert errors is None
    assert data is not None
    assert data.get('studentProfileCharacter') is not None
    assert data.get('studentProfileCharacter').get('success') is False

    errors = data.get('studentProfileCharacter').get('errors')
    assert errors is not None
    assert 'softSkills' in errors
    assert 'culturalFits' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert len(user.student.soft_skills.all()) == 0
    assert len(user.student.cultural_fits.all()) == 0


@pytest.mark.django_db
def test_character_with_too_many_soft_skills_and_cultural_fits(login, user_student,
                                                               student_character,
                                                               soft_skill_objects,
                                                               cultural_fit_objects):
    login(user_student)
    data, errors = student_character(user_student, soft_skill_objects[:7], cultural_fit_objects[:7])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileCharacter') is not None
    assert data.get('studentProfileCharacter').get('success') is False

    errors = data.get('studentProfileCharacter').get('errors')
    assert errors is not None
    assert 'softSkills' in errors
    assert 'culturalFits' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert len(user.student.soft_skills.all()) == 0
    assert len(user.student.cultural_fits.all()) == 0


@pytest.mark.django_db
def test_character_with_empty_soft_skills_and_cultural_fits(login, user_student, student_character):
    login(user_student)
    data, errors = student_character(user_student, [], [])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileCharacter') is not None
    assert data.get('studentProfileCharacter').get('success') is True

    errors = data.get('studentProfileCharacter').get('errors')
    assert errors is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert len(user.student.soft_skills.all()) == 0
    assert len(user.student.cultural_fits.all()) == 0
