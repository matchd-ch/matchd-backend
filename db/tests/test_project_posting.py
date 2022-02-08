from datetime import datetime

import pytest

from db.models.company import Company
from db.models.employee import Employee
from db.models.project_type import ProjectType
from db.models.project_posting import ProjectPosting
from db.models.student import Student
from db.models.topic import Topic


@pytest.mark.django_db
def test_create_project_posting(project_posting_valid_args):
    project_posting = ProjectPosting.objects.create(**project_posting_valid_args)

    assert isinstance(project_posting, ProjectPosting)


@pytest.mark.django_db
def test_get_project_posting(project_posting_valid_args):
    project_posting = ProjectPosting.objects.create(**project_posting_valid_args)
    project_posting = ProjectPosting.objects.get(id=project_posting.id)

    assert isinstance(project_posting, ProjectPosting)
    assert isinstance(project_posting.project_type, ProjectType)
    assert isinstance(project_posting.topic, Topic)
    assert isinstance(project_posting.employee, Employee)
    assert isinstance(project_posting.student, Student)
    assert isinstance(project_posting.company, Company)
    assert isinstance(project_posting.date_created, datetime)

    assert project_posting.title == project_posting_valid_args.get('title')
    assert project_posting.slug == project_posting_valid_args.get('slug')
    assert project_posting.keywords.count() == 0


@pytest.mark.django_db
def test_update_project_posting(project_posting_valid_args):
    new_title = 'A project'
    project_posting = ProjectPosting.objects.create(**project_posting_valid_args)
    ProjectPosting.objects.filter(id=project_posting.id).update(title=new_title)
    project_posting.refresh_from_db()

    assert isinstance(project_posting, ProjectPosting)
    assert isinstance(project_posting.title, str)

    assert project_posting.title == new_title


@pytest.mark.django_db
def test_delete_project_posting(project_posting_valid_args):
    project_posting = ProjectPosting.objects.create(**project_posting_valid_args)
    number_of_deletions, _ = project_posting.delete()

    assert number_of_deletions == 1
