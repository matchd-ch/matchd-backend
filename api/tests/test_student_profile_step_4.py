import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import Skill, Language, LanguageLevel, Hobby, OnlineProject, UserLanguageRelation

# pylint: disable=R0913


@pytest.mark.django_db
def test_step_4(login, user_student, student_step_4, skill_objects, language_objects, language_level_objects):
    user_student.student.profile_step = 4
    user_student.student.save()
    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, (
        (language_objects[0], language_level_objects[0]),
        (language_objects[1], language_level_objects[0]),
        (language_objects[0], language_level_objects[1])  # duplicate language
    ), [{'name': 'hobby'}, {'name': 'hobby 2'}], [{'url': 'www.google.com'}, {'url': 'www.google2.com'}], 'distinction')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    skills = user.student.skills.all()
    for obj in skill_objects[:6]:
        assert obj in skills
    # test if only two languages was added (third language is duplicate)
    languages = user.student.languages.all()
    assert len(languages) == 2
    hobbies = user.student.hobbies.all()
    assert len(hobbies) == 2
    online_projects = user.student.online_projects.all()
    assert len(online_projects) == 2
    assert user.student.distinction == 'distinction'
    assert user_student.student.profile_step == 5


@pytest.mark.django_db
def test_step_4_without_login(user_student, student_step_4, skill_objects, language_objects, language_level_objects):
    data, errors = student_step_4(AnonymousUser(), skill_objects, ((language_objects[0], language_level_objects[0]),),
                                  None, None, '')
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileStep4') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert len(user.student.soft_skills.all()) == 0
    assert len(user.student.cultural_fits.all()) == 0


@pytest.mark.django_db
def test_step_4_as_company(login, user_employee, student_step_4, skill_objects, language_objects,
                           language_level_objects):
    login(user_employee)
    data, errors = student_step_4(user_employee, skill_objects, ((language_objects[0], language_level_objects[0]),),
                                  None, None, '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None

    errors = data.get('studentProfileStep4').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_4_invalid_step(login, user_student, student_step_4, skill_objects, language_objects,
                             language_level_objects):
    user_student.student.profile_step = 0
    user_student.student.save()
    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, ((language_objects[0], language_level_objects[0]),),
                                  None, None, '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success') is False

    errors = data.get('studentProfileStep4').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.profile_step == 0


@pytest.mark.django_db
def test_step_4_with_invalid_data(login, user_student, student_step_4):
    user_student.student.profile_step = 4
    user_student.student.save()
    login(user_student)
    data, errors = student_step_4(user_student, [Skill(id=1337)], (
        (Language(id=1337, short_list=True), LanguageLevel(id=1337)),  # invalid languages are automatically ignored
    ), [{'name': ''}, {'name': 'hobby 2'}], [{'url': ''}, {'url': 'www.google2.com'}], 'a' * 1001)
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success') is False

    errors = data.get('studentProfileStep4').get('errors')
    assert errors is not None
    assert 'skills' in errors
    assert 'name' in errors
    assert 'url' in errors
    assert 'distinction' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert len(user.student.skills.all()) == 0
    assert len(user.student.languages.all()) == 0
    assert user_student.student.profile_step == 4


@pytest.mark.django_db
def test_step_4_update_delete_hobbies(login, user_student, student_step_4, skill_objects):
    user_student.student.profile_step = 4
    Hobby.objects.create(id=1, name='hobby 1', student=user_student.student)
    Hobby.objects.create(id=2, name='hobby 2', student=user_student.student)
    user_student.student.save()
    assert len(user_student.student.hobbies.all()) == 2

    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, [], [{'id': 1, 'name': 'hobby edited'}], [], '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    hobbies = user.student.hobbies.all()
    assert len(hobbies) == 1
    assert hobbies[0].id == 1
    assert hobbies[0].name == 'hobby edited'
    assert user_student.student.profile_step == 5


@pytest.mark.django_db
def test_step_4_update_delete_online_projects(login, user_student, student_step_4, skill_objects):
    user_student.student.profile_step = 4
    OnlineProject.objects.create(id=1, url='http://www.project1.lo', student=user_student.student)
    OnlineProject.objects.create(id=2, url='http://www.project2.lo', student=user_student.student)
    user_student.student.save()
    assert len(user_student.student.online_projects.all()) == 2

    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, [], [],
                                  [{'id': 1, 'url': 'http://www.project1-edited.lo'}], '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    online_projects = user.student.online_projects.all()
    assert len(online_projects) == 1
    assert online_projects[0].id == 1
    assert online_projects[0].url == 'http://www.project1-edited.lo'
    assert user_student.student.profile_step == 5


@pytest.mark.django_db
def test_step_4_update_delete_languages(login, user_student, student_step_4, skill_objects, language_objects,
                                        language_level_objects):
    user_student.student.profile_step = 4
    UserLanguageRelation.objects.create(id=1, student=user_student.student, language=language_objects[0],
                                        language_level=language_level_objects[0])
    UserLanguageRelation.objects.create(id=2, student=user_student.student, language=language_objects[1],
                                        language_level=language_level_objects[0])
    user_student.student.save()
    assert len(user_student.student.languages.all()) == 2

    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, (
        (language_objects[0], language_level_objects[1]),
    ), [], [], '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    languages = user.student.languages.all()
    assert len(languages) == 1
    assert languages[0].language.id == language_objects[0].id
    assert languages[0].language_level.id == language_level_objects[1].id
    assert user_student.student.profile_step == 5


@pytest.mark.django_db
def test_step_4_unique_hobbies_update(login, user_student, student_step_4, skill_objects):
    user_student.student.profile_step = 4
    Hobby.objects.create(id=1, name='hobby 1', student=user_student.student)
    Hobby.objects.create(id=2, name='hobby 2', student=user_student.student)
    user_student.student.save()
    assert len(user_student.student.hobbies.all()) == 2

    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, [],
                                  [{'id': 1, 'name': 'hobby 1'}, {'id': 2, 'name': 'hobby 1'}], [], '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success') is False

    errors = data.get('studentProfileStep4').get('errors')
    assert errors is not None
    assert 'nonFieldErrors' in errors
    assert errors.get('nonFieldErrors')[0].get('code') == 'unique_together'


@pytest.mark.django_db
def test_step_4_unique_hobbies_create(login, user_student, student_step_4, skill_objects):
    user_student.student.profile_step = 4
    Hobby.objects.create(id=1, name='hobby 1', student=user_student.student)
    user_student.student.save()
    assert len(user_student.student.hobbies.all()) == 1

    login(user_student)
    # new hobby should be ignored
    data, errors = student_step_4(user_student, skill_objects, [], [{'id': 1, 'name': 'hobby 1'}, {'name': 'hobby 1'}],
                                  [], '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    hobbies = user.student.hobbies.all()
    assert len(hobbies) == 1
    assert hobbies[0].id == 1
    assert hobbies[0].name == 'hobby 1'
    assert user_student.student.profile_step == 5


@pytest.mark.django_db
def test_step_4_unique_online_projects_update(login, user_student, student_step_4, skill_objects):
    user_student.student.profile_step = 4
    OnlineProject.objects.create(id=1, url='http://www.project1.lo', student=user_student.student)
    OnlineProject.objects.create(id=2, url='http://www.project2.lo', student=user_student.student)
    user_student.student.save()
    assert len(user_student.student.online_projects.all()) == 2

    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, [], [],
                              [{'id': 1, 'url': 'http://www.project1.lo'}, {'id': 2, 'url': 'http://www.project1.lo'}],
                              '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success') is False

    errors = data.get('studentProfileStep4').get('errors')
    assert errors is not None
    assert 'nonFieldErrors' in errors
    assert errors.get('nonFieldErrors')[0].get('code') == 'unique_together'


@pytest.mark.django_db
def test_step_4_unique_online_projects_create(login, user_student, student_step_4, skill_objects):
    user_student.student.profile_step = 4
    OnlineProject.objects.create(id=1, url='http://www.project1.lo', student=user_student.student)
    user_student.student.save()
    assert len(user_student.student.online_projects.all()) == 1

    login(user_student)
    data, errors = student_step_4(user_student, skill_objects, [], [],
                              [{'id': 1, 'url': 'http://www.project1.lo'}, {'url': 'http://www.project1.lo'}],
                              '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep4') is not None
    assert data.get('studentProfileStep4').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    online_projects = user.student.online_projects.all()
    assert len(online_projects) == 1
    assert online_projects[0].id == 1
    assert online_projects[0].url == 'http://www.project1.lo'
    assert user_student.student.profile_step == 5
