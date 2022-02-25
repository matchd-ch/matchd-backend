from graphql_relay import from_global_id
import pytest

from django.contrib.auth.models import AnonymousUser

from db.models import JobPosting, JobRequirement, Skill, Language, LanguageLevel

# pylint: disable=R0913


@pytest.mark.django_db
def test_requirements(user_employee, job_posting_object, login, job_posting_requirements,
                      job_requirement_objects, skill_objects, language_shortlist_objects,
                      language_no_shortlist_objects, language_level_objects):
    login(user_employee)
    job_posting_object.form_step = 2
    job_posting_object.save()
    data, errors = job_posting_requirements(
        user_employee,
        job_posting_object.id,
        job_requirement_objects,
        skill_objects,
        (
            (language_shortlist_objects[0],
             language_level_objects[0]),    # valid language (short list)
            (language_shortlist_objects[1],
             language_level_objects[0]),    # valid language (short list)
            (language_no_shortlist_objects[0], language_level_objects[1])    # invalid language
        ))
    assert errors is None
    assert data is not None
    assert data.get('jobPostingRequirements') is not None
    assert data.get('jobPostingRequirements').get('success')

    slug = data.get('jobPostingRequirements').get('slug')
    element_id = from_global_id(data.get('jobPostingRequirements').get('jobPostingId'))[1]

    job_posting_slug = JobPosting.objects.get(slug=slug)
    job_posting = JobPosting.objects.get(pk=element_id)
    assert job_posting_slug == job_posting

    job_requirements = job_posting.job_requirements.all()
    for obj in job_requirement_objects:
        assert obj in job_requirements
    skills = job_posting.skills.all()
    for obj in skill_objects:
        assert obj in skills
    languages = job_posting.languages.all()
    assert len(languages) == 2
    for language in languages:
        assert language.language in language_shortlist_objects
    assert job_posting.form_step == 3


@pytest.mark.django_db
def test_requirements_with_invalid_job_posting_id(user_employee, login, job_posting_requirements,
                                                  job_requirement_objects, skill_objects,
                                                  language_shortlist_objects,
                                                  language_level_objects):
    login(user_employee)
    data, errors = job_posting_requirements(
        user_employee, 1337, job_requirement_objects, skill_objects,
        ((language_shortlist_objects[0], language_level_objects[0]), ))
    assert errors is not None
    assert data is not None
    assert data.get('jobPostingRequirements') is None


@pytest.mark.django_db
def test_requirements_without_login(job_posting_requirements, job_posting_object,
                                    job_requirement_objects, skill_objects,
                                    language_shortlist_objects, language_level_objects):
    data, errors = job_posting_requirements(
        AnonymousUser(), job_posting_object.id, job_requirement_objects, skill_objects,
        ((language_shortlist_objects[0], language_level_objects[0]), ))

    assert errors is not None
    assert data is not None
    assert data.get('jobPostingRequirements') is None


@pytest.mark.django_db
def test_requirements_as_student(user_student, login, job_posting_requirements, job_posting_object,
                                 job_requirement_objects, skill_objects, language_shortlist_objects,
                                 language_level_objects):
    login(user_student)
    data, errors = job_posting_requirements(
        user_student, job_posting_object.id, job_requirement_objects, skill_objects,
        ((language_shortlist_objects[0], language_level_objects[0]), ))
    assert errors is None
    assert data is not None
    assert data.get('jobPostingRequirements') is not None
    assert data.get('jobPostingRequirements').get('success') is False
    assert data.get('jobPostingRequirements').get('slug') is None

    errors = data.get('jobPostingRequirements').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_requirements_as_employee_from_another_company(user_employee_2, job_posting_object, login,
                                                       job_posting_requirements,
                                                       job_requirement_objects, skill_objects,
                                                       language_shortlist_objects,
                                                       language_level_objects):
    login(user_employee_2)
    job_posting_object.form_step = 2
    job_posting_object.save()
    data, errors = job_posting_requirements(
        user_employee_2, job_posting_object.id, job_requirement_objects, skill_objects,
        ((language_shortlist_objects[0], language_level_objects[0]), ))
    assert errors is None
    assert data is not None
    assert data.get('jobPostingRequirements') is not None
    assert data.get('jobPostingRequirements').get('success') is False
    assert data.get('jobPostingRequirements').get('slug') is None

    errors = data.get('jobPostingRequirements').get('errors')
    assert errors is not None
    assert 'employee' in errors


@pytest.mark.django_db
def test_requirements_with_invalid_data(user_employee, job_posting_object, login,
                                        job_posting_requirements):
    login(user_employee)
    job_posting_object.form_step = 2
    job_posting_object.save()
    data, errors = job_posting_requirements(
        user_employee, job_posting_object.id, [JobRequirement(id=1337)], [Skill(id=1337)],
        ((Language(id=1337, short_list=True), LanguageLevel(id=1337)), ))
    assert errors is None
    assert data is not None
    assert data.get('jobPostingRequirements') is not None
    assert data.get('jobPostingRequirements').get('success') is False

    errors = data.get('jobPostingRequirements').get('errors')
    assert errors is not None
    assert 'jobRequirements' in errors
    assert 'skills' in errors
    # no check for languages here, invalid languages will be ignored

    job_posting = JobPosting.objects.get(pk=job_posting_object.id)
    assert job_posting.form_step == 2


@pytest.mark.django_db
def test_requirements_with_invalid_step(user_employee, job_posting_object, login,
                                        job_posting_requirements):
    login(user_employee)
    job_posting_object.form_step = 1
    job_posting_object.save()
    data, errors = job_posting_requirements(user_employee, job_posting_object.id, [], [], [])
    assert errors is None
    assert data is not None
    assert data.get('jobPostingRequirements') is not None
    assert data.get('jobPostingRequirements').get('success') is False

    errors = data.get('jobPostingRequirements').get('errors')
    assert errors is not None
    assert 'jobPostingStep' in errors
