import pytest

from graphql_relay import to_global_id

from db.models import Company, ProfileState, ProfileType, Employee

# pylint: disable=W0621
# pylint: disable=R0913
# pylint: disable=C0209


def company_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Company {
                name
                slug
            }
        }
    }
    '''


def company_query(slug):
    return '''
    query{
        company(slug: "%s"){
            id
            uid
            type
            name
            displayName
            slug
            zip
            city
            street
            phone
            website
            description
            services
            memberItStGallen
            state
            benefits {
                edges {
                    node {
                        id
                        icon
                    }
                }
            }
            branches {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
            employees {
                id
                role
                email
                firstName
                lastName
                phone
            }
            softSkills {
                id
                student
                company
            }
            culturalFits {
                id
                student
                company
            }
            jobPostings {
                id
            }
            challenges {
                id
            }
            topLevelOrganisationDescription
            topLevelOrganisationWebsite
            linkEducation
            linkChallenges
            linkThesis
        }
    }
    ''' % slug


def update_company_mutation():
    return '''
    mutation CompanyMutation($input: UpdateCompanyMutationInput!) {
      updateCompany(input: $input) {
        success,
        errors,
        company {
            id
            name
            state
        }
      }
    }
    '''


@pytest.fixture
def query_company_node(execute):

    def closure(user, id_value):
        return execute(company_node_query(),
                       variables={'id': to_global_id('Company', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_company(execute):

    def closure(user, slug):
        return execute(company_query(slug), **{'user': user})

    return closure


@pytest.fixture
def company_objects():
    return [
        Company.objects.create(name='Company 1', slug='company-1', type=ProfileType.COMPANY),
        Company.objects.create(name='Company 2', slug='company-2', type=ProfileType.COMPANY)
    ]


@pytest.fixture
def company_object(company_objects):
    return company_objects[0]


@pytest.fixture
def company_object_complete(user_employee, branch_objects, soft_skill_objects, benefit_objects,
                            cultural_fit_objects):
    company = user_employee.company
    company.state = ProfileState.PUBLIC
    company.slug = 'company-1'
    company.name = 'Company 1'
    company.zip = '1337'
    company.city = 'nowhere'
    company.street = 'street 1337'
    company.phone = '+41711234567'
    company.website = 'https://www.1337.lo'
    company.description = 'description'
    company.soft_skills.set(soft_skill_objects[:6])
    company.uid = 'CHE-000.000.000'
    company.services = 'services'
    company.member_it_st_gallen = True
    company.benefits.set(benefit_objects)
    company.branches.set(branch_objects)
    company.cultural_fits.set(cultural_fit_objects[:6])
    company.top_level_organisation_description = 'top level description'
    company.top_level_organisation_website = 'https://www.top-level.lo'
    company.link_education = 'https://edu.lo'
    company.link_challenges = 'https://challenges.lo'
    company.link_thesis = 'https://thesis.lo'
    company.save()
    return company


@pytest.fixture
def company_object_2(company_objects):
    return company_objects[1]


@pytest.fixture
def user_employee(get_user, default_password, company_object):
    user = get_user('employee-1@matchd.test', default_password, True, ProfileType.COMPANY,
                    company_object)

    Employee.objects.create(user=user)
    return user


@pytest.fixture
def user_employee_2(get_user, default_password, company_object_2):
    user = get_user('employee-2@matchd.test', default_password, True, ProfileType.COMPANY,
                    company_object_2)
    Employee.objects.create(user=user)
    return user


@pytest.fixture
def university_objects():
    return [
        Company.objects.create(name='University 1',
                               slug='university-1',
                               type=ProfileType.UNIVERSITY),
        Company.objects.create(name='University 2',
                               slug='university-2',
                               type=ProfileType.UNIVERSITY)
    ]


@pytest.fixture
def university_object(university_objects):
    return university_objects[0]


@pytest.fixture
def university_object_2(university_objects):
    return university_objects[1]


@pytest.fixture
def user_rector(get_user, default_password, university_object):
    user = get_user('rector-1@matchd.test', default_password, True, ProfileType.UNIVERSITY,
                    university_object)
    Employee.objects.create(user=user)
    return user


@pytest.fixture
def user_rector_2(get_user, default_password, university_object_2):
    user = get_user('rector-2@matchd.test', default_password, True, ProfileType.UNIVERSITY,
                    university_object_2)
    Employee.objects.create(user=user)
    return user


@pytest.fixture
def update_company(execute):

    def closure(user, company_data):
        return execute(update_company_mutation(),
                       variables={"input": {
                           **company_data
                       }},
                       **{'user': user})

    return closure
