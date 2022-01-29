from django.contrib.auth.models import AnonymousUser

import pytest

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_soft_skills, soft_skill_objects):
    data, errors = query_soft_skills(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('softSkills').get('edges')
    assert edges is not None
    assert len(edges) == len(soft_skill_objects)
    assert_node_id(edges[0].get('node'), 'SoftSkill', soft_skill_objects[0].id)
    assert_node_id(edges[1].get('node'), 'SoftSkill', soft_skill_objects[1].id)
    assert_node_field(edges[0].get('node'), 'student', soft_skill_objects[0].student)
    assert_node_field(edges[0].get('node'), 'company', soft_skill_objects[0].company)
    assert_node_field(edges[1].get('node'), 'student', soft_skill_objects[1].student)
    assert_node_field(edges[1].get('node'), 'company', soft_skill_objects[1].company)


@pytest.mark.django_db
def test_node_query(query_soft_skill_node, soft_skill_objects):
    data, errors = query_soft_skill_node(AnonymousUser(), soft_skill_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'SoftSkill', soft_skill_objects[0].id)
    assert_node_field(node, 'student', soft_skill_objects[0].student)
    assert_node_field(node, 'company', soft_skill_objects[0].company)
