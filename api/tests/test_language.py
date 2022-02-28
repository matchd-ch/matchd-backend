import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helper.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_languages, language_objects):
    data, errors = query_languages(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('languages').get('edges')
    assert edges is not None
    assert len(edges) == len(language_objects)
    assert_node_id(edges[0].get('node'), 'Language', language_objects[1].id)
    assert_node_id(edges[1].get('node'), 'Language', language_objects[2].id)
    assert_node_id(edges[2].get('node'), 'Language', language_objects[3].id)
    assert_node_id(edges[3].get('node'), 'Language', language_objects[0].id)
    assert_node_field(edges[0].get('node'), 'name', language_objects[1].name)
    assert_node_field(edges[1].get('node'), 'name', language_objects[2].name)
    assert_node_field(edges[2].get('node'), 'name', language_objects[3].name)
    assert_node_field(edges[3].get('node'), 'name', language_objects[0].name)


@pytest.mark.django_db
def test_shortlist_query(query_languages_shortlist, language_shortlist_objects):
    data, errors = query_languages_shortlist(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('languages').get('edges')
    assert edges is not None
    assert len(edges) == len(language_shortlist_objects)
    assert_node_id(edges[0].get('node'), 'Language', language_shortlist_objects[0].id)
    assert_node_id(edges[1].get('node'), 'Language', language_shortlist_objects[1].id)
    assert_node_field(edges[0].get('node'), 'name', language_shortlist_objects[0].name)
    assert_node_field(edges[1].get('node'), 'name', language_shortlist_objects[1].name)


@pytest.mark.django_db
def test_node_query(query_language_node, language_objects):
    data, errors = query_language_node(AnonymousUser(), language_objects[1].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'Language', language_objects[1].id)
    assert_node_field(node, 'name', language_objects[1].name)
