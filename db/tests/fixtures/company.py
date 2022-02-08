import uuid
import pytest

from db.models.company import Company
from db.models.profile_state import ProfileState
from db.models.profile_type import ProfileType


@pytest.fixture
def company_valid_args():
    return {
        'type': ProfileType.COMPANY,
        'state': ProfileState.PUBLIC,
        'profile_step': 1,
        'slug': 'acme',
        'name': 'ACME GmbH',
        'zip': '33100',
        'city': '9000',
        'street': 'Somestrasse 52',
        'phone': '0279929444',
        'website': 'www.acme.ch',
        'description': 'Company that builds special software.',
        'uid': str(uuid.uuid1()),
        'services': 'Software development, Tech Consulting',
        'member_it_st_gallen': 1,
    }


@pytest.fixture
def university_valid_args():
    return {
        'type': ProfileType.UNIVERSITY,
        'state': ProfileState.PUBLIC,
        'profile_step': 1,
        'slug': 'unigood',
        'name': 'Good University',
        'zip': '33100',
        'city': '9000',
        'street': 'Universitätstraße 50',
        'phone': '0279929444',
        'website': 'www.gooduni.ch',
        'description': 'Good university to study in.',
        'top_level_organisation_description': 'Good uni.',
        'top_level_organisation_website': 'www.gooduni.ch',
        'link_education': 'www.gooduni.ch/education',
        'link_projects': 'www.gooduni.ch/projects',
        'link_thesis': 'www.gooduni.ch/thesis',
    }


@pytest.fixture
def create_company():
    return Company.objects.create(name='Company 101', slug='company-101', type=ProfileType.COMPANY)


@pytest.fixture
def create_university():
    return Company.objects.create(name='University 101',
                                  slug='university-101',
                                  type=ProfileType.UNIVERSITY)
