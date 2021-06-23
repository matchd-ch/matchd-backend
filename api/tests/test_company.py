import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileState, JobPostingState, ProjectPostingState


@pytest.mark.django_db
def test_company(company_object_complete, query_company, job_posting_objects, company_project_posting_objects):
    for job_posting in job_posting_objects:
        job_posting.company = company_object_complete
        job_posting.save()

    for project_posting in company_project_posting_objects:
        project_posting.company = company_object_complete
        project_posting.save()

    data, errors = query_company(AnonymousUser(), company_object_complete.slug)

    company = data.get('company')
    assert errors is None
    assert company is not None
    assert company.get('type') == company_object_complete.type.upper()
    assert company.get('state') == company_object_complete.state.upper()
    assert company.get('profileStep') == company_object_complete.profile_step
    assert company.get('slug') == company_object_complete.slug
    assert company.get('name') == 'Company 1'
    assert company.get('displayName') == 'Com\xadpa\xadny 1'
    assert company.get('zip') == company_object_complete.zip
    assert company.get('city') == company_object_complete.city
    assert company.get('street') == company_object_complete.street
    assert company.get('phone') == company_object_complete.phone
    assert company.get('website') == company_object_complete.website
    assert company.get('description') == company_object_complete.description
    assert company.get('softSkills') is None  # soft skills should not be public
    assert company.get('uid') == company_object_complete.uid
    assert company.get('services') == company_object_complete.services
    assert company.get('memberItStGallen') == company_object_complete.member_it_st_gallen
    assert len(company.get('benefits')) == len(company_object_complete.benefits.all())
    assert len(company.get('branches')) == len(company_object_complete.branches.all())
    assert company.get('culturalFits') is None  # cultural fits should not be public
    assert company.get('topLevelOrganisationDescription') == company_object_complete.top_level_organisation_description
    assert company.get('topLevelOrganisationWebsite') == company_object_complete.top_level_organisation_website
    assert company.get('linkEducation') == company_object_complete.link_education
    assert company.get('linkProjects') == company_object_complete.link_projects
    assert company.get('linkThesis') == company_object_complete.link_thesis
    assert len(company.get('employees')) == len(company_object_complete.users.all())
    assert len(company.get('jobPostings')) == len(company_object_complete.job_postings.filter(
        state=JobPostingState.PUBLIC))
    assert len(company.get('projectPostings')) == len(company_object_complete.project_postings.filter(
        state=ProjectPostingState.PUBLIC))

    employee = company.get('employees')[0]
    assert employee.get('phone') == company.get('phone')


@pytest.mark.django_db
def test_company_incomplete(company_object_complete, query_company):
    company_object_complete.state = ProfileState.INCOMPLETE
    company_object_complete.save()
    data, errors = query_company(AnonymousUser(), company_object_complete.slug)
    company = data.get('company')
    assert company is None
    assert errors is not None


@pytest.mark.django_db
def test_company_incomplete_as_employee(login, company_object_complete, query_company):
    company_object_complete.state = ProfileState.INCOMPLETE
    company_object_complete.save()
    employee = company_object_complete.users.all().first()
    login(employee)
    data, errors = query_company(employee, company_object_complete.slug)
    company = data.get('company')
    assert errors is None
    assert company is not None
    assert company.get('type') == company_object_complete.type.upper()
    assert company.get('state') == company_object_complete.state.upper()
    assert company.get('profileStep') == company_object_complete.profile_step
    assert company.get('slug') == company_object_complete.slug
    assert company.get('name') == 'Company 1'
    assert company.get('displayName') == 'Com\xadpa\xadny 1'
    assert company.get('zip') == company_object_complete.zip
    assert company.get('city') == company_object_complete.city
    assert company.get('street') == company_object_complete.street
    assert company.get('phone') == company_object_complete.phone
    assert company.get('website') == company_object_complete.website
    assert company.get('description') == company_object_complete.description
    assert len(company.get('softSkills')) == len(company_object_complete.soft_skills.all())
    assert company.get('uid') == company_object_complete.uid
    assert company.get('services') == company_object_complete.services
    assert company.get('memberItStGallen') == company_object_complete.member_it_st_gallen
    assert len(company.get('benefits')) == len(company_object_complete.benefits.all())
    assert len(company.get('branches')) == len(company_object_complete.branches.all())
    assert len(company.get('culturalFits')) == len(company_object_complete.cultural_fits.all())
    assert company.get('topLevelOrganisationDescription') == company_object_complete.top_level_organisation_description
    assert company.get('topLevelOrganisationWebsite') == company_object_complete.top_level_organisation_website
    assert company.get('linkEducation') == company_object_complete.link_education
    assert company.get('linkProjects') == company_object_complete.link_projects
    assert company.get('linkThesis') == company_object_complete.link_thesis
    assert len(company.get('employees')) == len(company_object_complete.users.all())
    assert len(company.get('jobPostings')) == len(company_object_complete.job_postings.all())
    assert len(company.get('projectPostings')) == len(company_object_complete.project_postings.all())

    employee = company.get('employees')[0]
    assert employee.get('phone') == company.get('phone')
