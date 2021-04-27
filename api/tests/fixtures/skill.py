import pytest

from db.models import Skill


def skills_query():
    return '''
    query {
        skills {
            id
            name
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
def query_skills(execute):
    def closure(user):
        return execute(skills_query(), **{'user': user})
    return closure
