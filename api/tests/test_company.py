import pytest

from django.contrib.auth.models import AnonymousUser

from graphql_relay import to_global_id

from api.tests.helper.node_helper import assert_node_field, assert_node_id
from db.models import ProfileState, JobPostingState, ChallengeState


@pytest.mark.django_db
def test_company(company_object_complete, query_company, job_posting_objects,
                 company_challenge_objects):
    for job_posting in job_posting_objects:
        job_posting.company = company_object_complete
        job_posting.save()

    for challenge in company_challenge_objects:
        challenge.company = company_object_complete
        challenge.save()

    data, errors = query_company(AnonymousUser(), company_object_complete.slug)
    company = data.get('company')
    assert errors is None
    assert company is not None
    assert company.get('id') == to_global_id('Company', company_object_complete.id)
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
    assert company.get('softSkills') is None    # soft skills should not be public
    assert company.get('uid') == company_object_complete.uid
    assert company.get('services') == company_object_complete.services
    assert company.get('memberItStGallen') == company_object_complete.member_it_st_gallen
    assert len(company.get('benefits').get('edges')) == len(company_object_complete.benefits.all())
    assert len(company.get('branches').get('edges')) == len(company_object_complete.branches.all())
    assert company.get('culturalFits') is None    # cultural fits should not be public
    assert company.get('topLevelOrganisationDescription'
                       ) == company_object_complete.top_level_organisation_description
    assert company.get(
        'topLevelOrganisationWebsite') == company_object_complete.top_level_organisation_website
    assert company.get('linkEducation') == company_object_complete.link_education
    assert company.get('linkChallenges') == company_object_complete.link_challenges
    assert company.get('linkThesis') == company_object_complete.link_thesis
    assert len(company.get('employees')) == len(company_object_complete.users.all())
    assert len(company.get('jobPostings')) == len(
        company_object_complete.job_postings.filter(state=JobPostingState.PUBLIC))
    assert len(company.get('challenges')) == len(
        company_object_complete.challenges.filter(state=ChallengeState.PUBLIC))

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
    assert company.get('id') == to_global_id('Company', company_object_complete.id)
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
    assert len(company.get('benefits').get('edges')) == len(company_object_complete.benefits.all())
    assert len(company.get('branches').get('edges')) == len(company_object_complete.branches.all())
    assert len(company.get('culturalFits')) == len(company_object_complete.cultural_fits.all())
    assert company.get('topLevelOrganisationDescription'
                       ) == company_object_complete.top_level_organisation_description
    assert company.get(
        'topLevelOrganisationWebsite') == company_object_complete.top_level_organisation_website
    assert company.get('linkEducation') == company_object_complete.link_education
    assert company.get('linkChallenges') == company_object_complete.link_challenges
    assert company.get('linkThesis') == company_object_complete.link_thesis
    assert len(company.get('employees')) == len(company_object_complete.users.all())
    assert len(company.get('jobPostings')) == len(company_object_complete.job_postings.all())
    assert len(company.get('challenges')) == len(company_object_complete.challenges.all())

    employee = company.get('employees')[0]
    assert employee.get('phone') == company.get('phone')


@pytest.mark.django_db
def test_node_query(query_company_node, company_object_complete):
    data, errors = query_company_node(AnonymousUser(), company_object_complete.id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'Company', company_object_complete.id)
    assert_node_field(node, 'name', company_object_complete.name)
    assert_node_field(node, 'slug', company_object_complete.slug)


@pytest.mark.django_db
def test_update_company(login, company_object_complete, update_company):
    employee = company_object_complete.users.all().first()
    login(employee)

    name = "New Name"
    state = "ANONYMOUS"

    company_data = {
        'id': to_global_id('Company', company_object_complete.id),
        'name': name,
        'state': state
    }

    data, errors = update_company(employee, company_data)
    assert data is not None
    assert errors is None
    assert data.get('updateCompany').get('success')
    assert data.get('updateCompany').get('errors') is None

    assert data.get('updateCompany').get('company').get('name') == name
    assert data.get('updateCompany').get('company').get('state') == state
