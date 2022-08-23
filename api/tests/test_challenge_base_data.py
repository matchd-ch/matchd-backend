import pytest

from graphql_relay import from_global_id

from django.contrib.auth.models import AnonymousUser

from db.models import Challenge, ChallengeType, Keyword, ProfileType

# pylint: disable=R0913
# pylint: disable=C0301


@pytest.mark.django_db
def test_base_data_as_company(user_employee, login, challenge_base_data, challenge_type_objects,
                              keyword_objects):
    _test_base_data(user_employee, login, challenge_base_data, challenge_type_objects,
                    keyword_objects)


@pytest.mark.django_db
def test_base_data_as_student(user_student, login, challenge_base_data, challenge_type_objects,
                              keyword_objects):
    _test_base_data(user_student, login, challenge_base_data, challenge_type_objects,
                    keyword_objects)


def _test_base_data(user, login, challenge_base_data, challenge_type_objects, keyword_objects):
    login(user)
    data, errors = challenge_base_data(user, 'title', 'description', 5, 'to be defined',
                                       challenge_type_objects[0], keyword_objects)

    assert errors is None
    assert data is not None
    assert data.get('challengeBaseData') is not None
    assert data.get('challengeBaseData').get('success')

    slug = data.get('challengeBaseData').get('slug')
    element_id = from_global_id(data.get('challengeBaseData').get('challengeId'))[1]

    challenge_slug = Challenge.objects.get(slug=slug)
    challenge = Challenge.objects.get(pk=element_id)

    assert challenge_slug == challenge
    assert challenge.title == 'title'
    assert challenge.slug == f'title-{str(challenge.id)}'
    assert challenge.description == 'description'
    assert challenge.team_size == 5
    assert challenge.compensation == 'to be defined'
    assert challenge.challenge_type == challenge_type_objects[0]
    assert len(challenge.keywords.all()) == len(keyword_objects)
    if user.type in ProfileType.valid_company_types():
        assert challenge.employee.id == user.employee.id
        assert challenge.company.id == user.company.id
        assert challenge.student is None
    if user.type in ProfileType.valid_student_types():
        assert challenge.student.id == user.student.id
        assert challenge.employee is None
        assert challenge.company is None
    assert challenge.form_step == 2


@pytest.mark.django_db
def test_base_data_without_login(challenge_base_data, challenge_type_objects, keyword_objects):
    data, errors = challenge_base_data(AnonymousUser(), 'title', 'description', 5, 'No description',
                                       challenge_type_objects[0], keyword_objects)
    assert errors is not None
    assert data is not None
    assert data.get('challengeBaseData') is None


@pytest.mark.django_db
def test_base_data_with_invalid_data(user_employee, login, challenge_base_data):
    login(user_employee)
    data, errors = challenge_base_data(user_employee, '', '', 0, '', ChallengeType(id=1337),
                                       [Keyword(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('challengeBaseData') is not None
    assert data.get('challengeBaseData').get('success') is False
    assert data.get('challengeBaseData').get('slug') is None

    errors = data.get('challengeBaseData').get('errors')
    assert errors is not None
    assert 'title' in errors
    assert 'description' in errors
    assert 'teamSize' in errors
    assert 'compensation' in errors
    assert 'challengeType' in errors
    assert 'keywords' in errors
