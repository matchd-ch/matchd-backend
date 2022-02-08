import pytest

from db.models.soft_skill import SoftSkill


@pytest.mark.django_db
def test_create_soft_skill(soft_skill_valid_args):
    soft_skill = SoftSkill.objects.create(**soft_skill_valid_args)

    assert isinstance(soft_skill, SoftSkill)


@pytest.mark.django_db
def test_get_soft_skill(soft_skill_valid_args):
    soft_skill = SoftSkill.objects.create(**soft_skill_valid_args)
    soft_skill = SoftSkill.objects.get(id=soft_skill.id)

    assert isinstance(soft_skill, SoftSkill)
    assert isinstance(soft_skill.student, str)
    assert isinstance(soft_skill.company, str)

    assert soft_skill.student == soft_skill_valid_args.get('student')
    assert soft_skill.company == soft_skill_valid_args.get('company')


@pytest.mark.django_db
def test_update_soft_skill(soft_skill_valid_args):
    new_company = 'Leadership'
    soft_skill = SoftSkill.objects.create(**soft_skill_valid_args)
    SoftSkill.objects.filter(id=soft_skill.id).update(company=new_company)
    soft_skill.refresh_from_db()

    assert isinstance(soft_skill, SoftSkill)
    assert isinstance(soft_skill.company, str)

    assert soft_skill.company == new_company


@pytest.mark.django_db
def test_delete_soft_skill(soft_skill_valid_args):
    soft_skill = SoftSkill.objects.create(**soft_skill_valid_args)
    number_of_deletions, _ = soft_skill.delete()

    assert number_of_deletions == 1
