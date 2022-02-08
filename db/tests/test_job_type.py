import pytest

from db.models.job_type import JobType


@pytest.mark.django_db
def test_create_job_isinstance(job_type_valid_args):
    job_type = JobType.objects.create(**job_type_valid_args)

    assert isinstance(job_type, JobType)


@pytest.mark.django_db
def test_get_job_isinstance(job_type_valid_args):
    job_type = JobType.objects.create(**job_type_valid_args)
    job_type = JobType.objects.get(id=job_type.id)

    assert isinstance(job_type, JobType)
    assert isinstance(job_type.name, str)
    assert isinstance(job_type.mode, str)

    assert job_type.name == job_type_valid_args.get('name')
    assert job_type.mode == job_type_valid_args.get('mode')


@pytest.mark.django_db
def test_update_job_isinstance(job_type_valid_args):
    new_name = 'Advanced working'
    job_type = JobType.objects.create(**job_type_valid_args)
    JobType.objects.filter(id=job_type.id).update(name=new_name)
    job_type.refresh_from_db()

    assert isinstance(job_type, JobType)
    assert isinstance(job_type.name, str)

    assert job_type.name == new_name


@pytest.mark.django_db
def test_delete_job_isinstance(job_type_valid_args):
    job_type = JobType.objects.create(**job_type_valid_args)
    number_of_deletions, _ = job_type.delete()

    assert number_of_deletions == 1
