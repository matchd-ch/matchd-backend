import pytest

from graphql_relay import to_global_id

# pylint: disable=R0913
# pylint: disable=C0209


def university_profile_mutation(kind):
    return '''
    mutation UniversityProfileMutation($input: UniversityProfile%sInput!) {
        universityProfile%s(input: $input) {
            success,
            errors
        }
    }
    ''' % (kind, kind)


@pytest.fixture
def university_base_data(execute):

    def closure(user, first_name, last_name, name, street, zip_value, city, phone, role, website,
                top_level_organisation_website, top_level_organisation_description):
        return execute(university_profile_mutation("BaseData"),
                       variables={
                           'input': {
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
        return execute(university_profile_mutation("SpecificData"),
                       variables={'input': {
                           'description': description,
                       }},
                       **{'user': user})

    return closure


@pytest.fixture
def university_relations(execute):

    def closure(user, services, link_education, link_challenges, link_thesis, branches, benefits):
        return execute(university_profile_mutation("Relations"),
                       variables={
                           'input': {
                               'services':
                               services,
                               'linkEducation':
                               link_education,
                               'linkChallenges':
                               link_challenges,
                               'linkThesis':
                               link_thesis,
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
def university_values(execute):

    def closure(user, soft_skills, cultural_fits):
        return execute(university_profile_mutation("Values"),
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
