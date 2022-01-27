from django.contrib.auth.models import AnonymousUser

import pytest

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_benefits, benefit_objects):
    data, errors = query_benefits(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('benefits').get('edges')
    assert edges is not None
    assert len(edges) == len(benefit_objects)

    assert_node_id(edges[0].get('node'), f'Benefit:{benefit_objects[1].id}')
    assert_node_id(edges[1].get('node'), f'Benefit:{benefit_objects[0].id}')
    assert_node_field(edges[0].get('node'), 'name', benefit_objects[1].name)
    assert_node_field(edges[1].get('node'), 'name', benefit_objects[0].name)


@pytest.mark.django_db
def test_node_query(query_benefit_node, benefit_objects):
    data, errors = query_benefit_node(AnonymousUser(), f'Benefit:{benefit_objects[0].id}')

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, f'Benefit:{benefit_objects[0].id}')
    assert_node_field(node, 'name', benefit_objects[0].name)
