import pytest

# pylint: disable=W0621
# pylint: disable=R0913
# pylint: disable=C0209


def student_profile_mutation(step):
    step = str(step)
    return '''
    mutation StudentProfileMutation($step%s: StudentProfileInputStep%s!) {
        studentProfileStep%s(step%s: $step%s) {
            success,
            errors
        }
    }
    ''' % (step, step, step, step, step)


def student_profile_mutation_step_5():
    return '''
    mutation StudentProfileMutation($step5: StudentProfileInputStep5!) {
        studentProfileStep5(step5: $step5) {
            success,
            errors,
            nicknameSuggestions
        }
    }
    '''


@pytest.fixture
def student_step_1(execute):
    def closure(user, first_name, last_name, street, zip_value, city, date_of_birth, mobile):
        return execute(student_profile_mutation(1), variables={
            'step1': {
                'firstName': first_name,
                'lastName': last_name,
                'street': street,
                'zip': zip_value,
                'city': city,
                'dateOfBirth': date_of_birth,
                'mobile': mobile
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def student_step_2(execute):
    def closure(user, job_type, job_from_date, job_to_date, branch):
        return execute(student_profile_mutation(2), variables={
            'step2': {
                'jobType': {'id': job_type.id},
                'jobFromDate': job_from_date,
                'jobToDate': job_to_date,
                'branch': {'id': branch.id}
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def student_step_3(execute):
    def closure(user, soft_skills, cultural_fits):
        return execute(student_profile_mutation(3), variables={
            'step3': {
                'softSkills': [{'id': obj.id} for obj in soft_skills],
                'culturalFits': [{'id': obj.id} for obj in cultural_fits],
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def student_step_4(execute):
    def closure(user, skills, languages, hobbies, online_projects, distinction):
        return execute(student_profile_mutation(4), variables={
            'step4': {
                'skills': [{'id': obj.id} for obj in skills],
                'languages': [
                    {'language': obj[0].id, 'languageLevel': obj[1].id}
                    for obj in languages
                ],
                'hobbies': hobbies,
                'onlineProjects': online_projects,
                'distinction': distinction
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def student_step_5(execute):
    def closure(user, nickname):
        return execute(student_profile_mutation_step_5(), variables={
            'step5': {
                'nickname': nickname
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def student_step_6(execute):
    def closure(user, state):
        return execute(student_profile_mutation(6), variables={
            'step6': {
                'state': state
            }
        }, **{'user': user})
    return closure
