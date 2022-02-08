import pytest

from db.models.job_requirement import JobRequirement


@pytest.mark.django_db
def test_create_job_requirement(job_requirement_valid_args):
    job_requirement = JobRequirement.objects.create(**job_requirement_valid_args)

    assert isinstance(job_requirement, JobRequirement)


@pytest.mark.django_db
def test_get_job_requirement(job_requirement_valid_args):
    job_requirement = JobRequirement.objects.create(**job_requirement_valid_args)
    job_requirement = JobRequirement.objects.get(id=job_requirement.id)

    assert isinstance(job_requirement, JobRequirement)
    assert isinstance(job_requirement.name, str)

    assert job_requirement.name == job_requirement_valid_args.get('name')


@pytest.mark.django_db
def test_update_job_requirement(job_requirement_valid_args):
    new_name = 'passion'
    job_requirement = JobRequirement.objects.create(**job_requirement_valid_args)
    JobRequirement.objects.filter(id=job_requirement.id).update(name=new_name)
    job_requirement.refresh_from_db()

    assert isinstance(job_requirement, JobRequirement)
    assert isinstance(job_requirement.name, str)

    assert job_requirement.name == new_name


@pytest.mark.django_db
def test_delete_job_requirement(job_requirement_valid_args):
    job_requirement = JobRequirement.objects.create(**job_requirement_valid_args)
    number_of_deletions, _ = job_requirement.delete()

    assert number_of_deletions == 1
