import pytest

from graphql_relay import to_global_id

# pylint: disable=W0621
# pylint: disable=R0913
# pylint: disable=C0209


def student_profile_mutation(kind):
    return '''
    mutation StudentProfileMutation($input: StudentProfile%sInput!) {
        studentProfile%s(input: $input) {
            success,
            errors
        }
    }
    ''' % (kind, kind)


def student_profile_mutation_specific_data():
    return '''
    mutation StudentProfileMutation($input: StudentProfileSpecificDataInput!) {
        studentProfileSpecificData(input: $input) {
            success,
            errors,
            nicknameSuggestions
        }
    }
    '''


@pytest.fixture
def student_base_data(execute):

    def closure(user, first_name, last_name, street, zip_value, city, date_of_birth, mobile):
        return execute(student_profile_mutation("BaseData"),
                       variables={
                           'input': {
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
        return execute(student_profile_mutation("Employment"),
                       variables={
                           'input': {
                               'jobType': {
                                   'id': to_global_id('JobType', job_type.id)
                               },
                               'jobFromDate': job_from_date,
                               'jobToDate': job_to_date,
                               'branch': {
                                   'id': to_global_id('Branch', branch.id)
                               }
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def student_character(execute):

    def closure(user, soft_skills, cultural_fits):
        return execute(student_profile_mutation("Character"),
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


@pytest.fixture
def student_abilities(execute):

    def closure(user, skills, languages, hobbies, online_challenges, distinction):
        languages = languages if languages else []
        hobbies = hobbies if hobbies else []
        online_challenges = online_challenges if online_challenges else []
        return execute(
            student_profile_mutation("Abilities"),
            variables={
                'input': {
                    'skills': [{
                        'id': to_global_id('Skill', obj.id)
                    } for obj in skills],
                    'languages': [{
                        'language': to_global_id('Language', obj[0].id),
                        'languageLevel': to_global_id('LanguageLevel', obj[1].id)
                    } for obj in languages],
                    'hobbies': [
                        __updated_dict(obj, {'id': to_global_id('Hobby', obj['id'])})
                        if 'id' in obj else obj for obj in hobbies
                    ],
                    'onlineChallenges': [
                        __updated_dict(obj, {'id': to_global_id('OnlineChallenge', obj['id'])})
                        if 'id' in obj else obj for obj in online_challenges
                    ],
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
                       variables={'input': {
                           'nickname': nickname
                       }},
                       **{'user': user})

    return closure


@pytest.fixture
def student_condition(execute):

    def closure(user, state):
        return execute(student_profile_mutation("Condition"),
                       variables={'input': {
                           'state': state
                       }},
                       **{'user': user})

    return closure


def __updated_dict(dictionary, keyval):
    dictionary.update(keyval)
    return dictionary
