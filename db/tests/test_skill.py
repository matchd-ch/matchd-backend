import pytest

from db.models.skill import Skill


@pytest.mark.django_db
def test_create_skill(skill_valid_args):
    skill = Skill.objects.create(**skill_valid_args)

    assert isinstance(skill, Skill)


@pytest.mark.django_db
def test_get_skill(skill_valid_args):
    skill = Skill.objects.create(**skill_valid_args)
    skill = Skill.objects.get(id=skill.id)

    assert isinstance(skill, Skill)
    assert isinstance(skill.name, str)

    assert skill.name == skill_valid_args.get('name')


@pytest.mark.django_db
def test_update_skill(skill_valid_args):
    new_name = 'rich'
    skill = Skill.objects.create(**skill_valid_args)
    Skill.objects.filter(id=skill.id).update(name=new_name)
    skill.refresh_from_db()

    assert isinstance(skill, Skill)
    assert isinstance(skill.name, str)

    assert skill.name == new_name


@pytest.mark.django_db
def test_delete_skill(skill_valid_args):
    skill = Skill.objects.create(**skill_valid_args)
    number_of_deletions, _ = skill.delete()

    assert number_of_deletions == 1
