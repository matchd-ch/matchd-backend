import pytest

from db.models.online_project import OnlineProject
from db.models.student import Student


@pytest.mark.django_db
def test_create_online_project(online_project_valid_args):
    online_project = OnlineProject.objects.create(**online_project_valid_args)

    assert isinstance(online_project, OnlineProject)


@pytest.mark.django_db
def test_get_online_project(online_project_valid_args):
    online_project = OnlineProject.objects.create(**online_project_valid_args)
    online_project = OnlineProject.objects.get(id=online_project.id)

    assert isinstance(online_project, OnlineProject)
    assert isinstance(online_project.url, str)
    assert isinstance(online_project.student, Student)

    assert online_project.url == online_project_valid_args.get('url')
    assert online_project.student.slug == online_project_valid_args.get('student').slug


@pytest.mark.django_db
def test_update_online_project(online_project_valid_args):
    new_url = 'www.awesomejob.ch'
    online_project = OnlineProject.objects.create(**online_project_valid_args)
    OnlineProject.objects.filter(id=online_project.id).update(url=new_url)
    online_project.refresh_from_db()

    assert isinstance(online_project, OnlineProject)
    assert isinstance(online_project.url, str)

    assert online_project.url == new_url


@pytest.mark.django_db
def test_delete_online_project(online_project_valid_args):
    online_project = OnlineProject.objects.create(**online_project_valid_args)
    number_of_deletions, _ = online_project.delete()

    assert number_of_deletions == 1
