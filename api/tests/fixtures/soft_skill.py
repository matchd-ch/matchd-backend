import pytest

from db.models import SoftSkill


def soft_skills_query():
    return '''
    query {
        softSkills {
            id
            student
            company
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
        SoftSkill.objects.create(id=7, student="I like apples", company='You like apples')
    ]


@pytest.fixture
def query_soft_skills(execute):
    def closure(user):
        return execute(soft_skills_query(), **{'user': user})
    return closure
