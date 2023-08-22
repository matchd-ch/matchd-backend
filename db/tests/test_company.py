import pytest

from db.models.company import Company


@pytest.mark.django_db
def test_create_company(company_valid_args):
    company = Company.objects.create(**company_valid_args)

    assert isinstance(company, Company)


@pytest.mark.django_db
def test_get_company(company_valid_args):
    company = Company.objects.create(**company_valid_args)
    company = Company.objects.get(id=company.id)

    assert isinstance(company, Company)
    assert isinstance(company.type, str)
    assert isinstance(company.state, str)
    assert isinstance(company.slug, str)
    assert isinstance(company.name, str)
    assert isinstance(company.zip, str)
    assert isinstance(company.city, str)
    assert isinstance(company.street, str)
    assert isinstance(company.phone, str)
    assert isinstance(company.website, str)
    assert isinstance(company.description, str)
    assert isinstance(company.uid, str)
    assert isinstance(company.services, str)
    assert isinstance(company.member_it_st_gallen, bool)

    assert company.branches.count() == 0
    assert company.soft_skills.count() == 0
    assert company.benefits.count() == 0
    assert company.cultural_fits.count() == 0

    assert company.type == company_valid_args.get('type')
    assert company.state == company_valid_args.get('state')
    assert company.slug == company_valid_args.get('slug')
    assert company.name == company_valid_args.get('name')
    assert company.zip == company_valid_args.get('zip')
    assert company.city == company_valid_args.get('city')
    assert company.street == company_valid_args.get('street')
    assert company.phone == company_valid_args.get('phone')
    assert company.website == company_valid_args.get('website')
    assert company.description == company_valid_args.get('description')
    assert company.uid == company_valid_args.get('uid')
    assert company.services == company_valid_args.get('services')
    assert company.member_it_st_gallen == company_valid_args.get('member_it_st_gallen')

    # Fields that a company should not have
    assert company.top_level_organisation_description == ''
    assert company.top_level_organisation_website == ''
    assert company.link_education is None
    assert company.link_challenges is None
    assert company.link_thesis is None


@pytest.mark.django_db
def test_update_company(company_valid_args):
    new_name = 'ACME LLC'
    company = Company.objects.create(**company_valid_args)
    Company.objects.filter(id=company.id).update(name=new_name)
    company.refresh_from_db()

    assert isinstance(company, Company)
    assert isinstance(company.name, str)

    assert company.name == new_name


@pytest.mark.django_db
def test_delete_company(company_valid_args):
    company = Company.objects.create(**company_valid_args)
    number_of_deletions, _ = company.delete()

    assert number_of_deletions == 1


@pytest.mark.django_db
def test_create_university(university_valid_args):
    university = Company.objects.create(**university_valid_args)

    assert isinstance(university, Company)


@pytest.mark.django_db
def test_get_university(university_valid_args):
    university = Company.objects.create(**university_valid_args)
    university = Company.objects.get(id=university.id)

    assert isinstance(university, Company)
    assert isinstance(university.type, str)
    assert isinstance(university.state, str)
    assert isinstance(university.slug, str)
    assert isinstance(university.name, str)
    assert isinstance(university.zip, str)
    assert isinstance(university.city, str)
    assert isinstance(university.street, str)
    assert isinstance(university.phone, str)
    assert isinstance(university.website, str)
    assert isinstance(university.description, str)
    assert isinstance(university.top_level_organisation_description, str)
    assert isinstance(university.top_level_organisation_website, str)
    assert isinstance(university.link_education, str)
    assert isinstance(university.link_challenges, str)
    assert isinstance(university.link_thesis, str)

    assert university.branches.count() == 0

    assert university.type == university_valid_args.get('type')
    assert university.state == university_valid_args.get('state')
    assert university.slug == university_valid_args.get('slug')
    assert university.name == university_valid_args.get('name')
    assert university.zip == university_valid_args.get('zip')
    assert university.city == university_valid_args.get('city')
    assert university.street == university_valid_args.get('street')
    assert university.phone == university_valid_args.get('phone')
    assert university.website == university_valid_args.get('website')
    assert university.description == university_valid_args.get('description')
    assert university.top_level_organisation_description == university_valid_args.get(
        'top_level_organisation_description')
    assert university.top_level_organisation_website == university_valid_args.get(
        'top_level_organisation_website')
    assert university.link_education == university_valid_args.get('link_education')
    assert university.link_challenges == university_valid_args.get('link_challenges')
    assert university.link_thesis == university_valid_args.get('link_thesis')
    assert university.member_it_st_gallen is False

    # Fields that a university should not have
    assert university.uid == ''
    assert university.services == ''
    assert university.soft_skills.count() == 0
    assert university.benefits.count() == 0
    assert university.cultural_fits.count() == 0
