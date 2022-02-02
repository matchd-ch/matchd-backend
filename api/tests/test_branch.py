import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_branches, branch_objects):
    data, errors = query_branches(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('branches').get('edges')
    assert edges is not None
    assert len(edges) == len(branch_objects)
    assert_node_id(edges[0].get('node'), 'Branch', branch_objects[1].id)
    assert_node_id(edges[1].get('node'), 'Branch', branch_objects[0].id)
    assert_node_field(edges[0].get('node'), 'name', branch_objects[1].name)
    assert_node_field(edges[1].get('node'), 'name', branch_objects[0].name)


@pytest.mark.django_db
def test_node_query(query_branch_node, branch_objects):
    data, errors = query_branch_node(AnonymousUser(), branch_objects[1].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'Branch', branch_objects[1].id)
    assert_node_field(node, 'name', branch_objects[1].name)
