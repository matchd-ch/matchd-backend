import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import SoftSkill


def soft_skill_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on SoftSkill {
                student
                company
            }
        }
    }
    ''' % b64_encoded_id


def soft_skills_query():
    return '''
    query {
        softSkills(first: 12) {
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
                    student
                    company
                }
            }
        }
    }
    '''


@pytest.fixture
def soft_skill_objects():
    return [
        SoftSkill.objects.create(id=1, student="I like working", company='You like working'),
        SoftSkill.objects.create(id=2, student="I like things", company='You like things'),
        SoftSkill.objects.create(id=3, student="I like stuff", company='You like stuff'),
        SoftSkill.objects.create(id=4, student="I like beer", company='You like beer'),
        SoftSkill.objects.create(id=5, student="I like honey", company='You like honey'),
        SoftSkill.objects.create(id=6, student="I like flowers", company='You like flowers'),
        SoftSkill.objects.create(id=7, student="I like apples", company='You like apples'),
        SoftSkill.objects.create(id=8, student="I like bushes", company='You like bushes'),
        SoftSkill.objects.create(id=9, student="I like ants", company='You like ants'),
        SoftSkill.objects.create(id=10, student="I like lions", company='You like lions'),
        SoftSkill.objects.create(id=11, student="I like everything", company='You like everything'),
        SoftSkill.objects.create(id=12, student="I like nothing", company='You like nothing')
    ]


@pytest.fixture
def query_soft_skill_node(execute):
    def closure(user, node_id):
        return execute(soft_skill_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_soft_skills(execute):
    def closure(user):
        return execute(soft_skills_query(), **{'user': user})
    return closure
