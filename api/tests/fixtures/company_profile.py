import pytest

# pylint: disable=R0913
# pylint: disable=C0209


def company_profile_mutation(kind, gql_variable_name):
    return '''
    mutation CompanyProfileMutation($%s: CompanyProfileInput%s!) {
        companyProfile%s(%s: $%s) {
            success,
            errors
        }
    }
    ''' % (gql_variable_name, kind, kind, gql_variable_name, gql_variable_name)


@pytest.fixture
def company_base_data(execute):

    def closure(user, first_name, last_name, name, street, zip_value, city, phone, role):
        return execute(company_profile_mutation("BaseData", "baseData"),
                       variables={
                           'baseData': {
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
        return execute(company_profile_mutation("Relations", "relations"),
                       variables={
                           'relations': {
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
        return execute(company_profile_mutation("Advantages", "advantages"),
                       variables={
                           'advantages': {
                               'branches': [{
                                   'id': obj.id
                               } for obj in branches],
                               'benefits': [{
                                   'id': obj.id
                               } for obj in benefits],
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def company_values(execute):

    def closure(user, soft_skills, cultural_fits):
        return execute(company_profile_mutation("Values", "values"),
                       variables={
                           'values': {
                               'softSkills': [{
                                   'id': obj.id
                               } for obj in soft_skills],
                               'culturalFits': [{
                                   'id': obj.id
                               } for obj in cultural_fits],
                           }
                       },
                       **{'user': user})

    return closure
