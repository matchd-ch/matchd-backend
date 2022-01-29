import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_language_levels, language_level_objects):
    data, errors = query_language_levels(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('languageLevels').get('edges')
    assert edges is not None
    assert len(edges) == len(language_level_objects)
    assert_node_id(edges[0].get('node'), 'LanguageLevel', language_level_objects[0].id)
    assert_node_id(edges[1].get('node'), 'LanguageLevel', language_level_objects[2].id)
    assert_node_id(edges[2].get('node'), 'LanguageLevel', language_level_objects[1].id)
    assert_node_field(edges[0].get('node'), 'level', language_level_objects[0].level)
    assert_node_field(edges[1].get('node'), 'level', language_level_objects[2].level)
    assert_node_field(edges[2].get('node'), 'level', language_level_objects[1].level)


@pytest.mark.django_db
def test_node_query(query_language_level_node, language_level_objects):
    data, errors = query_language_level_node(AnonymousUser(), language_level_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'LanguageLevel', language_level_objects[0].id)
    assert_node_field(node, 'level', language_level_objects[0].level)
