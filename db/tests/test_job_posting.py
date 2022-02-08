from datetime import datetime

import pytest

from db.models.company import Company
from db.models.employee import Employee
from db.models.job_type import JobType
from db.models.job_posting import JobPosting


@pytest.mark.django_db
def test_create_job_posting(job_posting_valid_args):
    job_posting = JobPosting.objects.create(**job_posting_valid_args)

    assert isinstance(job_posting, JobPosting)


@pytest.mark.django_db
def test_get_job_posting(job_posting_valid_args):
    job_posting = JobPosting.objects.create(**job_posting_valid_args)
    job_posting = JobPosting.objects.get(id=job_posting.id)

    assert isinstance(job_posting, JobPosting)
    assert isinstance(job_posting.job_type, JobType)
    assert isinstance(job_posting.company, Company)
    assert isinstance(job_posting.employee, Employee)
    assert isinstance(job_posting.date_created, datetime)

    assert job_posting.title == job_posting_valid_args.get('title')
    assert job_posting.slug == job_posting_valid_args.get('slug')
    assert job_posting.description == job_posting_valid_args.get('description')


@pytest.mark.django_db
def test_update_job_posting(job_posting_valid_args):
    new_title = 'Perfect title'
    job_posting = JobPosting.objects.create(**job_posting_valid_args)
    JobPosting.objects.filter(id=job_posting.id).update(title=new_title)
    job_posting.refresh_from_db()

    assert isinstance(job_posting, JobPosting)
    assert isinstance(job_posting.title, str)

    assert job_posting.title == new_title


@pytest.mark.django_db
def test_delete_job_posting(job_posting_valid_args):
    job_posting = JobPosting.objects.create(**job_posting_valid_args)
    number_of_deletions, _ = job_posting.delete()

    assert number_of_deletions == 1
