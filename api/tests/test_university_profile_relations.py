import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileState, SoftSkill, CulturalFit


@pytest.mark.django_db
def test_relations(login, user_rector, university_relations, branch_objects, benefit_objects):
    user_rector.company.profile_step = 3
    user_rector.company.save()
    login(user_rector)
    data, errors = university_relations(user_rector, 'services', 'http://edu.lo',
                                        'http://projects.lo', 'http://thesis.lo', branch_objects,
                                        benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileRelations') is not None
    assert data.get('universityProfileRelations').get('success')

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.services == 'services'
    assert user.company.link_education == 'http://edu.lo'
    assert user.company.link_projects == 'http://projects.lo'
    assert user.company.link_thesis == 'http://thesis.lo'
    assert len(user.company.branches.all()) == len(branch_objects)
    assert user.company.profile_step == 4
    assert user.company.state == ProfileState.INCOMPLETE


@pytest.mark.django_db
def test_relations_without_login(user_rector, university_relations, branch_objects,
                                 benefit_objects):
    user_rector.company.profile_step = 3
    user_rector.company.save()
    data, errors = university_relations(AnonymousUser(), 'services', 'http://edu.lo',
                                        'http://projects.lo', 'http://thesis.lo', branch_objects,
                                        benefit_objects)
    assert errors is not None
    assert data is not None
    assert data.get('universityProfileRelations') is None

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.services == ''
    assert user.company.link_education is None
    assert user.company.link_projects is None
    assert user.company.link_thesis is None
    assert len(user.company.branches.all()) == 0
    assert user.company.profile_step == 3


@pytest.mark.django_db
def test_relations_as_student(login, user_student, university_relations, branch_objects,
                              benefit_objects):
    login(user_student)
    data, errors = university_relations(user_student, 'services', 'http://edu.lo',
                                        'http://projects.lo', 'http://thesis.lo', branch_objects,
                                        benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileRelations') is not None

    errors = data.get('universityProfileRelations').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_relations_invalid_step(login, user_rector, university_relations, branch_objects,
                                benefit_objects):
    user_rector.company.profile_step = 0
    user_rector.company.save()
    login(user_rector)
    data, errors = university_relations(user_rector, 'services', 'http://edu.lo',
                                        'http://projects.lo', 'http://thesis.lo', branch_objects,
                                        benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileRelations') is not None
    assert data.get('universityProfileRelations').get('success') is False

    errors = data.get('universityProfileRelations').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.company.profile_step == 0


@pytest.mark.django_db
def test_relations_invalid_data(login, user_rector, university_relations):
    user_rector.company.profile_step = 3
    user_rector.company.save()
    login(user_rector)
    data, errors = university_relations(user_rector, 'a' * 301, 'invalid', 'invalid', 'invalid',
                                        [SoftSkill(id=1337)], [CulturalFit(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileRelations') is not None
    assert data.get('universityProfileRelations').get('success') is False

    errors = data.get('universityProfileRelations').get('errors')
    assert errors is not None
    assert 'services' in errors
    assert 'linkEducation' in errors
    assert 'linkProjects' in errors
    assert 'linkThesis' in errors
    assert 'branches' in errors
    assert 'benefits' in errors

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.company.profile_step == 3
