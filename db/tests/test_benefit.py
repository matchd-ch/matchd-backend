import pytest

from db.models.benefit import Benefit


@pytest.mark.django_db
def test_create_benefit(benefit_valid_args):
    benefit = Benefit.objects.create(**benefit_valid_args)

    assert isinstance(benefit, Benefit)


@pytest.mark.django_db
def test_get_benefit(benefit_valid_args):
    benefit = Benefit.objects.create(**benefit_valid_args)
    benefit = Benefit.objects.get(id=benefit.id)

    assert isinstance(benefit, Benefit)
    assert isinstance(benefit.name, str)
    assert isinstance(benefit.icon, str)

    assert benefit.name == benefit_valid_args.get('name')
    assert benefit.icon == benefit_valid_args.get('icon')


@pytest.mark.django_db
def test_update_benefit(benefit_valid_args):
    new_icon = 'dollar'
    benefit = Benefit.objects.create(**benefit_valid_args)
    Benefit.objects.filter(id=benefit.id).update(icon=new_icon)
    benefit.refresh_from_db()

    assert isinstance(benefit, Benefit)
    assert isinstance(benefit.name, str)

    assert benefit.icon == new_icon


@pytest.mark.django_db
def test_delete_benefit(benefit_valid_args):
    benefit = Benefit.objects.create(**benefit_valid_args)
    number_of_deletions, _ = benefit.delete()

    assert number_of_deletions == 1
