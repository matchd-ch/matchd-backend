import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileType

# pylint: disable=C0103


@pytest.mark.django_db
def test_me_company(login, me, user_employee, company_object_complete):
    user_employee.first_name = 'John'
    user_employee.last_name = 'Doe'
    user_employee.save()

    login(user_employee)
    data, errors = me(user_employee)
    assert errors is None
    assert data is not None

    user = data.get('me')
    assert user is not None
    assert user.get('username') == 'employee-1@matchd.test'
    assert user.get('email') == 'employee-1@matchd.test'
    assert user.get('firstName') == 'John'
    assert user.get('lastName') == 'Doe'
    assert user.get('type') == ProfileType.COMPANY.upper()

    company = user.get('company')
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

    student = user.get('student')
    assert student is None


@pytest.mark.django_db
def test_me_company_without_login(me):
    data, errors = me(AnonymousUser())
    assert errors is not None
    assert data is not None

    user = data.get('me')
    assert user is None
