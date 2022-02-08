import pytest

from db.models.job_posting import JobPosting
from db.models.language import Language
from db.models.language_level import LanguageLevel
from db.models.job_posting_language_relation import JobPostingLanguageRelation


@pytest.mark.django_db
def test_create_job_posting_language_relation(job_posting_language_relation_valid_args):
    job_posting_language_relation = JobPostingLanguageRelation.objects.create(
        **job_posting_language_relation_valid_args)

    assert isinstance(job_posting_language_relation, JobPostingLanguageRelation)


@pytest.mark.django_db
def test_get_job_posting_language_relation(job_posting_language_relation_valid_args):
    job_posting_language_relation = JobPostingLanguageRelation.objects.create(
        **job_posting_language_relation_valid_args)
    job_posting_language_relation = JobPostingLanguageRelation.objects.get(
        id=job_posting_language_relation.id)

    assert isinstance(job_posting_language_relation, JobPostingLanguageRelation)
    assert isinstance(job_posting_language_relation.job_posting, JobPosting)
    assert isinstance(job_posting_language_relation.language, Language)
    assert isinstance(job_posting_language_relation.language_level, LanguageLevel)

    assert job_posting_language_relation.job_posting == job_posting_language_relation_valid_args.get(
        'job_posting')
    assert job_posting_language_relation.language == job_posting_language_relation_valid_args.get(
        'language')
    assert job_posting_language_relation.language_level == job_posting_language_relation_valid_args.get(
        'language_level')


@pytest.mark.django_db
def test_update_job_posting_language_relation(job_posting_language_relation_valid_args,
                                              create_language):
    new_language = create_language('Italian')
    job_posting_language_relation = JobPostingLanguageRelation.objects.create(
        **job_posting_language_relation_valid_args)
    JobPostingLanguageRelation.objects.filter(id=job_posting_language_relation.id).update(
        language=new_language)
    job_posting_language_relation.refresh_from_db()

    assert isinstance(job_posting_language_relation, JobPostingLanguageRelation)
    assert isinstance(job_posting_language_relation.language, Language)

    assert job_posting_language_relation.language == new_language


@pytest.mark.django_db
def test_delete_job_posting_language_relation(job_posting_language_relation_valid_args):
    job_posting_language_relation = JobPostingLanguageRelation.objects.create(
        **job_posting_language_relation_valid_args)
    number_of_deletions, _ = job_posting_language_relation.delete()

    assert number_of_deletions == 1
