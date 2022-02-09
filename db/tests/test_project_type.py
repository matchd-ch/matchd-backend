import pytest

from db.models.project_type import ProjectType


@pytest.mark.django_db
def test_create_project_isinstance(project_type_valid_args):
    project_type = ProjectType.objects.create(**project_type_valid_args)

    assert isinstance(project_type, ProjectType)


@pytest.mark.django_db
def test_get_project_isinstance(project_type_valid_args):
    project_type = ProjectType.objects.create(**project_type_valid_args)
    project_type = ProjectType.objects.get(id=project_type.id)

    assert isinstance(project_type, ProjectType)
    assert isinstance(project_type.name, str)

    assert project_type.name == project_type_valid_args.get('name')


@pytest.mark.django_db
def test_update_project_isinstance(project_type_valid_args):
    new_name = 'rich'
    project_type = ProjectType.objects.create(**project_type_valid_args)
    ProjectType.objects.filter(id=project_type.id).update(name=new_name)
    project_type.refresh_from_db()

    assert isinstance(project_type, ProjectType)
    assert isinstance(project_type.name, str)

    assert project_type.name == new_name


@pytest.mark.django_db
def test_delete_project_isinstance(project_type_valid_args):
    project_type = ProjectType.objects.create(**project_type_valid_args)
    number_of_deletions, _ = project_type.delete()

    assert number_of_deletions == 1
