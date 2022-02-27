import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helper.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_skills, skill_objects):
    data, errors = query_skills(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('skills').get('edges')
    assert edges is not None
    assert len(edges) == len(skill_objects)
    assert_node_id(edges[0].get('node'), 'Skill', skill_objects[1].id)
    assert_node_id(edges[1].get('node'), 'Skill', skill_objects[2].id)
    assert_node_id(edges[2].get('node'), 'Skill', skill_objects[0].id)
    assert_node_id(edges[3].get('node'), 'Skill', skill_objects[3].id)
    assert_node_field(edges[0].get('node'), 'name', skill_objects[1].name)
    assert_node_field(edges[1].get('node'), 'name', skill_objects[2].name)
    assert_node_field(edges[2].get('node'), 'name', skill_objects[0].name)
    assert_node_field(edges[3].get('node'), 'name', skill_objects[3].name)


@pytest.mark.django_db
def test_node_query(query_skill_node, skill_objects):
    data, errors = query_skill_node(AnonymousUser(), skill_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'Skill', skill_objects[0].id)
    assert_node_field(node, 'name', skill_objects[0].name)
