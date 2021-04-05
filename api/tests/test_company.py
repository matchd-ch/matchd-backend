import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileState


@pytest.mark.django_db
def test_company(company_object_complete, query_company):
    data, errors = query_company(AnonymousUser(), company_object_complete.slug)
    company = data.get('company')
    assert errors is None
    assert company is not None
    assert company.get('type') == company_object_complete.type.upper()
    assert company.get('state') == company_object_complete.state.upper()
    assert company.get('profileStep') == company_object_complete.profile_step
    assert company.get('slug') == company_object_complete.slug
    assert company.get('name') == company_object_complete.name
    assert company.get('zip') == company_object_complete.zip
    assert company.get('city') == company_object_complete.city
    assert company.get('street') == company_object_complete.street
    assert company.get('phone') == company_object_complete.phone
    assert company.get('website') == company_object_complete.website
    assert int(company.get('branch').get('id')) == company_object_complete.branch.id
    assert company.get('description') == company_object_complete.description
    assert len(company.get('softSkills')) == len(company_object_complete.soft_skills.all())
    assert company.get('uid') == company_object_complete.uid
    assert company.get('services') == company_object_complete.services
    assert company.get('memberItStGallen') == company_object_complete.member_it_st_gallen
    assert len(company.get('benefits')) == len(company_object_complete.benefits.all())
    assert len(company.get('jobPositions')) == len(company_object_complete.job_positions.all())
    assert len(company.get('culturalFits')) == len(company_object_complete.cultural_fits.all())
    assert company.get('topLevelOrganisationDescription') == company_object_complete.top_level_organisation_description
    assert company.get('topLevelOrganisationWebsite') == company_object_complete.top_level_organisation_website
    assert company.get('linkEducation') == company_object_complete.link_education
    assert company.get('linkProjects') == company_object_complete.link_projects
    assert company.get('linkThesis') == company_object_complete.link_thesis
    assert len(company.get('employees')) == len(company_object_complete.users.all())


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
    assert company.get('name') == company_object_complete.name
    assert company.get('zip') == company_object_complete.zip
    assert company.get('city') == company_object_complete.city
    assert company.get('street') == company_object_complete.street
    assert company.get('phone') == company_object_complete.phone
    assert company.get('website') == company_object_complete.website
    assert int(company.get('branch').get('id')) == company_object_complete.branch.id
    assert company.get('description') == company_object_complete.description
    assert len(company.get('softSkills')) == len(company_object_complete.soft_skills.all())
    assert company.get('uid') == company_object_complete.uid
    assert company.get('services') == company_object_complete.services
    assert company.get('memberItStGallen') == company_object_complete.member_it_st_gallen
    assert len(company.get('benefits')) == len(company_object_complete.benefits.all())
    assert len(company.get('jobPositions')) == len(company_object_complete.job_positions.all())
    assert len(company.get('culturalFits')) == len(company_object_complete.cultural_fits.all())
    assert company.get('topLevelOrganisationDescription') == company_object_complete.top_level_organisation_description
    assert company.get('topLevelOrganisationWebsite') == company_object_complete.top_level_organisation_website
    assert company.get('linkEducation') == company_object_complete.link_education
    assert company.get('linkProjects') == company_object_complete.link_projects
    assert company.get('linkThesis') == company_object_complete.link_thesis
    assert len(company.get('employees')) == len(company_object_complete.users.all())
