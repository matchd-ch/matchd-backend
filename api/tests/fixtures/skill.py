import pytest

from graphql_relay import to_global_id

from db.models import Skill


def skill_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Skill {
                name
            }
        }
    }
    '''


def skills_query():
    return '''
    query {
        skills(first: 4) {
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    id
                    name
                }
            }
        }
    }
    '''


@pytest.fixture
def skill_objects():
    return [
        Skill.objects.create(name="php"),
        Skill.objects.create(name="css"),
        Skill.objects.create(name="java"),
        Skill.objects.create(name="python"),
    ]


@pytest.fixture
def query_skill_node(execute):

    def closure(user, id_value):
        return execute(skill_node_query(),
                       variables={'id': to_global_id('Skill', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_skills(execute):

    def closure(user):
        return execute(skills_query(), **{'user': user})

    return closure
