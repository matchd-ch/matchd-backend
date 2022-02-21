import pytest

# pylint: disable=W0621
# pylint: disable=R0913
# pylint: disable=C0209


def student_profile_mutation(kind, gql_variable_name):
    return '''
    mutation StudentProfileMutation($%s: StudentProfileInput%s!) {
        studentProfile%s(%s: $%s) {
            success,
            errors
        }
    }
    ''' % (gql_variable_name, kind, kind, gql_variable_name, gql_variable_name)


def student_profile_mutation_specific_data():
    return '''
    mutation StudentProfileMutation($specificData: StudentProfileInputSpecificData!) {
        studentProfileSpecificData(specificData: $specificData) {
            success,
            errors,
            nicknameSuggestions
        }
    }
    '''


@pytest.fixture
def student_base_data(execute):

    def closure(user, first_name, last_name, street, zip_value, city, date_of_birth, mobile):
        return execute(student_profile_mutation("BaseData", "baseData"),
                       variables={
                           'baseData': {
                               'firstName': first_name,
                               'lastName': last_name,
                               'street': street,
                               'zip': zip_value,
                               'city': city,
                               'dateOfBirth': date_of_birth,
                               'mobile': mobile
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def student_employment(execute):

    def closure(user, job_type, job_from_date, job_to_date, branch):
        return execute(student_profile_mutation("Employment", "employment"),
                       variables={
                           'employment': {
                               'jobType': {
                                   'id': job_type.id
                               },
                               'jobFromDate': job_from_date,
                               'jobToDate': job_to_date,
                               'branch': {
                                   'id': branch.id
                               }
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def student_character(execute):

    def closure(user, soft_skills, cultural_fits):
        return execute(student_profile_mutation("Character", "character"),
                       variables={
                           'character': {
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


@pytest.fixture
def student_abilities(execute):

    def closure(user, skills, languages, hobbies, online_projects, distinction):
        return execute(student_profile_mutation("Abilities", "abilities"),
                       variables={
                           'abilities': {
                               'skills': [{
                                   'id': obj.id
                               } for obj in skills],
                               'languages': [{
                                   'language': obj[0].id,
                                   'languageLevel': obj[1].id
                               } for obj in languages],
                               'hobbies':
                               hobbies,
                               'onlineProjects':
                               online_projects,
                               'distinction':
                               distinction
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def student_specific_data(execute):

    def closure(user, nickname):
        return execute(student_profile_mutation_specific_data(),
                       variables={'specificData': {
                           'nickname': nickname
                       }},
                       **{'user': user})

    return closure


@pytest.fixture
def student_condition(execute):

    def closure(user, state):
        return execute(student_profile_mutation("Condition", "condition"),
                       variables={'condition': {
                           'state': state
                       }},
                       **{'user': user})

    return closure
