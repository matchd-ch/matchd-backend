import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_keywords, keyword_objects):
    data, errors = query_keywords(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('keywords').get('edges')
    assert edges is not None
    assert len(edges) == len(keyword_objects)
    assert_node_id(edges[0].get('node'), f'Keyword:{keyword_objects[1].id}')
    assert_node_id(edges[1].get('node'), f'Keyword:{keyword_objects[0].id}')
    assert_node_field(edges[0].get('node'), 'name', keyword_objects[1].name)
    assert_node_field(edges[1].get('node'), 'name', keyword_objects[0].name)


@pytest.mark.django_db
def test_node_query(query_keyword_node, keyword_objects):
    data, errors = query_keyword_node(AnonymousUser(), f'Keyword:{keyword_objects[1].id}')

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, f'Keyword:{keyword_objects[1].id}')
    assert_node_field(node, 'name', keyword_objects[1].name)
