import datetime

from io import StringIO

import pytest

from django.core import management
from django.contrib.auth.models import AnonymousUser

from graphql_relay import to_global_id

from db.models import ProfileState


@pytest.mark.django_db
def test_challenges_filter_challenge_type(query_challenges, user_student_full_profile,
                                          company_challenge_objects, student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(
        AnonymousUser(), {
            'challengeTypeIds': [
                f"\"{to_global_id('ChallengeType', company_challenge_objects[0].challenge_type_id)}\"",
                f"\"{to_global_id('ChallengeType', company_challenge_objects[3].challenge_type_id)}\""
            ]
        })
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 6


@pytest.mark.django_db
def test_challenges_empty_filter_challenge_type(query_challenges, user_student_full_profile,
                                                company_challenge_objects,
                                                student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(AnonymousUser(), {'challengeTypeIds': []})
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 7


@pytest.mark.django_db
def test_challenges_filter_keywords(query_challenges, user_student_full_profile, keyword_objects,
                                    company_challenge_objects, student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    company_challenge_objects[0].keywords.set([obj.id for obj in keyword_objects])
    student_challenge_objects[1].keywords.set([keyword_objects[0].id])

    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(
        AnonymousUser(),
        {'keywordIds': [f"\"{to_global_id('Keywords', obj.id)}\"" for obj in keyword_objects]})
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 2


@pytest.mark.django_db
def test_challenges_empty_filter_keywords(query_challenges, user_student_full_profile,
                                          keyword_objects, company_challenge_objects,
                                          student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    company_challenge_objects[0].keywords.set([obj.id for obj in keyword_objects])
    student_challenge_objects[1].keywords.set([keyword_objects[0].id])

    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(AnonymousUser(), {'keywordIds': []})
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 7


@pytest.mark.django_db
def test_challenges_filter_team_size(query_challenges, user_student_full_profile,
                                     company_challenge_objects, student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    data, errors = query_challenges(AnonymousUser(), {'teamSize': 10})
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 1


@pytest.mark.django_db
def test_challenges_filter_challenge_from_date(query_challenges, user_student_full_profile,
                                               company_challenge_objects,
                                               student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    company_challenge_objects[0].challenge_from_date = datetime.datetime(2020, 3, 18).date()
    company_challenge_objects[0].save()

    student_challenge_objects[1].challenge_from_date = datetime.datetime(2020, 3, 18).date()

    student_challenge_objects[1].save()

    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(
        AnonymousUser(), {'challengeFromDate': f"\"{datetime.datetime(2020, 2, 20).date()}\""})
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 2


@pytest.mark.django_db
def test_challenges_filter_date_published(query_challenges, user_student_full_profile,
                                          company_challenge_objects, student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    student_challenge_objects[1].date_published = datetime.datetime(2020, 3, 18).date()
    student_challenge_objects[1].save()

    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(
        AnonymousUser(), {'datePublished': f"\"{datetime.datetime(2020, 2, 20).date()}\""})
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 1


@pytest.mark.django_db
def test_challenges_search_description(query_challenges, user_student_full_profile,
                                       company_challenge_objects, student_challenge_objects):
    data, errors = query_challenges(AnonymousUser(), {"textSearch": "\"two\""})
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 1
