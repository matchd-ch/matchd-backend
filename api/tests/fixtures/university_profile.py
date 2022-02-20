import pytest

# pylint: disable=R0913
# pylint: disable=C0209


def university_profile_mutation(kind, gql_variable_name):
    return '''
    mutation UniversityProfileMutation($%s: UniversityProfileInput%s!) {
        universityProfile%s(%s: $%s) {
            success,
            errors
        }
    }
    ''' % (gql_variable_name, kind, kind, gql_variable_name, gql_variable_name)


@pytest.fixture
def university_base_data(execute):

    def closure(user, first_name, last_name, name, street, zip_value, city, phone, role, website,
                top_level_organisation_website, top_level_organisation_description):
        return execute(university_profile_mutation("BaseData", "baseData"),
                       variables={
                           'baseData': {
                               'firstName': first_name,
                               'lastName': last_name,
                               'name': name,
                               'street': street,
                               'zip': zip_value,
                               'city': city,
                               'phone': phone,
                               'role': role,
                               'website': website,
                               'topLevelOrganisationWebsite': top_level_organisation_website,
                               'topLevelOrganisationDescription': top_level_organisation_description
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def university_specific_data(execute):

    def closure(user, description):
        return execute(university_profile_mutation("SpecificData", "specificData"),
                       variables={'specificData': {
                           'description': description,
                       }},
                       **{'user': user})

    return closure


@pytest.fixture
def university_relations(execute):

    def closure(user, services, link_education, link_projects, link_thesis, branches, benefits):
        return execute(university_profile_mutation("Relations", "relations"),
                       variables={
                           'relations': {
                               'services': services,
                               'linkEducation': link_education,
                               'linkProjects': link_projects,
                               'linkThesis': link_thesis,
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
def university_values(execute):

    def closure(user, soft_skills, cultural_fits):
        return execute(university_profile_mutation("Values", "values"),
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
