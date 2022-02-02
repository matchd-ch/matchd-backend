import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_project_types, project_type_objects):
    data, errors = query_project_types(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('projectTypes').get('edges')
    assert edges is not None
    assert len(edges) == len(project_type_objects)
    assert_node_id(edges[0].get('node'), 'ProjectType', project_type_objects[0].id)
    assert_node_id(edges[1].get('node'), 'ProjectType', project_type_objects[1].id)
    assert_node_field(edges[0].get('node'), 'name', project_type_objects[0].name)
    assert_node_field(edges[1].get('node'), 'name', project_type_objects[1].name)


@pytest.mark.django_db
def test_node_query(query_project_type_node, project_type_objects):
    data, errors = query_project_type_node(AnonymousUser(), project_type_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'ProjectType', project_type_objects[0].id)
    assert_node_field(node, 'name', project_type_objects[0].name)
