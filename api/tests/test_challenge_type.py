import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helper.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_challenge_types, challenge_type_objects):
    data, errors = query_challenge_types(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('challengeTypes').get('edges')
    assert edges is not None
    assert len(edges) == len(challenge_type_objects)
    assert_node_id(edges[0].get('node'), 'ChallengeType', challenge_type_objects[0].id)
    assert_node_id(edges[1].get('node'), 'ChallengeType', challenge_type_objects[1].id)
    assert_node_id(edges[2].get('node'), 'ChallengeType', challenge_type_objects[2].id)
    assert_node_field(edges[0].get('node'), 'name', challenge_type_objects[0].name)
    assert_node_field(edges[1].get('node'), 'name', challenge_type_objects[1].name)
    assert_node_field(edges[2].get('node'), 'name', challenge_type_objects[2].name)


@pytest.mark.django_db
def test_node_query(query_challenge_type_node, challenge_type_objects):
    data, errors = query_challenge_type_node(AnonymousUser(), challenge_type_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'ChallengeType', challenge_type_objects[0].id)
    assert_node_field(node, 'name', challenge_type_objects[0].name)
