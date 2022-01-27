import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import Skill


def skill_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on Skill {
                name
            }
        }
    }
    ''' % b64_encoded_id


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
    def closure(user, node_id):
        return execute(skill_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_skills(execute):
    def closure(user):
        return execute(skills_query(), **{'user': user})
    return closure
