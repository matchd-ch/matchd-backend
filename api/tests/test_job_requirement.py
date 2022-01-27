import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helpers.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_job_requirements, job_requirement_objects):
    data, errors = query_job_requirements(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('jobRequirements').get('edges')
    assert edges is not None
    assert len(edges) == len(job_requirement_objects)
    assert_node_id(edges[0].get('node'), f'JobRequirement:{job_requirement_objects[1].id}')
    assert_node_id(edges[1].get('node'), f'JobRequirement:{job_requirement_objects[0].id}')
    assert_node_field(edges[0].get('node'), 'name', job_requirement_objects[1].name)
    assert_node_field(edges[1].get('node'), 'name', job_requirement_objects[0].name)


@pytest.mark.django_db
def test_node_query(query_job_requirement_node, job_requirement_objects):
    data, errors = query_job_requirement_node(AnonymousUser(), f'JobRequirement:{job_requirement_objects[1].id}')

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, f'JobRequirement:{job_requirement_objects[1].id}')
    assert_node_field(node, 'name', job_requirement_objects[1].name)
