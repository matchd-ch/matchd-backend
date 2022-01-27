from django.contrib.auth.models import AnonymousUser

import pytest

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_cultural_fits, cultural_fit_objects):
    data, errors = query_cultural_fits(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('culturalFits').get('edges')
    assert edges is not None
    assert len(edges) == len(cultural_fit_objects)
    assert_node_id(edges[0].get('node'), f'CulturalFit:{cultural_fit_objects[0].id}')
    assert_node_id(edges[1].get('node'), f'CulturalFit:{cultural_fit_objects[1].id}')
    assert_node_field(edges[0].get('node'), 'student', cultural_fit_objects[0].student)
    assert_node_field(edges[0].get('node'), 'company', cultural_fit_objects[0].company)
    assert_node_field(edges[1].get('node'), 'student', cultural_fit_objects[1].student)
    assert_node_field(edges[1].get('node'), 'company', cultural_fit_objects[1].company)


@pytest.mark.django_db
def test_node_query(query_cultural_fit_node, cultural_fit_objects):
    data, errors = query_cultural_fit_node(AnonymousUser(), f'CulturalFit:{cultural_fit_objects[0].id}')

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, f'CulturalFit:{cultural_fit_objects[0].id}')
    assert_node_field(node, 'student', cultural_fit_objects[0].student)
    assert_node_field(node, 'company', cultural_fit_objects[0].company)
