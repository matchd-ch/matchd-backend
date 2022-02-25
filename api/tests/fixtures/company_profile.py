import pytest

from graphql_relay import to_global_id

# pylint: disable=R0913
# pylint: disable=C0209


def company_profile_mutation(kind):
    return '''
    mutation CompanyProfileMutation($input: CompanyProfile%sInput!) {
        companyProfile%s(input: $input) {
            success,
            errors
        }
    }
    ''' % (kind, kind)


@pytest.fixture
def company_base_data(execute):

    def closure(user, first_name, last_name, name, street, zip_value, city, phone, role):
        return execute(company_profile_mutation("BaseData"),
                       variables={
                           'input': {
                               'firstName': first_name,
                               'lastName': last_name,
                               'name': name,
                               'street': street,
                               'zip': zip_value,
                               'city': city,
                               'phone': phone,
                               'role': role
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def company_relations(execute):

    def closure(user, website, description, services, member_it_st_gallen):
        return execute(company_profile_mutation("Relations"),
                       variables={
                           'input': {
                               'website': website,
                               'description': description,
                               'services': services,
                               'memberItStGallen': member_it_st_gallen
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def company_advantages(execute):

    def closure(user, branches, benefits):
        return execute(company_profile_mutation("Advantages"),
                       variables={
                           'input': {
                               'branches': [{
                                   'id': to_global_id('Branch', obj.id)
                               } for obj in branches],
                               'benefits': [{
                                   'id': to_global_id('Benefit', obj.id)
                               } for obj in benefits],
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def company_values(execute):

    def closure(user, soft_skills, cultural_fits):
        return execute(company_profile_mutation("Values"),
                       variables={
                           'input': {
                               'softSkills': [{
                                   'id': to_global_id('SoftSkill', obj.id)
                               } for obj in soft_skills],
                               'culturalFits': [{
                                   'id': to_global_id('CulturalFit', obj.id)
                               } for obj in cultural_fits],
                           }
                       },
                       **{'user': user})

    return closure
