import pytest

from db.models.branch import Branch


@pytest.mark.django_db
def test_create_branch(branch_valid_args):
    branch = Branch.objects.create(**branch_valid_args)

    assert isinstance(branch, Branch)


@pytest.mark.django_db
def test_get_branch(branch_valid_args):
    branch = Branch.objects.create(**branch_valid_args)
    branch = Branch.objects.get(id=branch.id)

    assert isinstance(branch, Branch)
    assert isinstance(branch.name, str)

    assert branch.name == branch_valid_args.get('name')


@pytest.mark.django_db
def test_update_branch(branch_valid_args):
    new_name = 'rich'
    branch = Branch.objects.create(**branch_valid_args)
    Branch.objects.filter(id=branch.id).update(name=new_name)
    branch.refresh_from_db()

    assert isinstance(branch, Branch)
    assert isinstance(branch.name, str)

    assert branch.name == new_name


@pytest.mark.django_db
def test_delete_branch(branch_valid_args):
    branch = Branch.objects.create(**branch_valid_args)
    number_of_deletions, _ = branch.delete()

    assert number_of_deletions == 1
