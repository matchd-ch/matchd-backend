import pytest

# pylint: disable=R0913


def company_profile_mutation(step):
    step = str(step)
    return '''
    mutation CompanyProfileMutation($step%s: CompanyProfileInputStep%s!) {
        companyProfileStep%s(step%s: $step%s) {
            success,
            errors
        }
    }
    ''' % (step, step, step, step, step)


@pytest.fixture
def company_step_1(execute):
    def closure(user, first_name, last_name, name, street, zip_value, city, phone, role):
        return execute(company_profile_mutation(1), variables={
            'step1': {
                'firstName': first_name,
                'lastName': last_name,
                'name': name,
                'street': street,
                'zip': zip_value,
                'city': city,
                'phone': phone,
                'role': role
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def company_step_2(execute):
    def closure(user, website, description, services, member_it_st_gallen):
        return execute(company_profile_mutation(2), variables={
            'step2': {
                'website': website,
                'description': description,
                'services': services,
                'memberItStGallen': member_it_st_gallen
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def company_step_3(execute):
    def closure(user, branches, benefits):
        return execute(company_profile_mutation(3), variables={
            'step3': {
                'branches': [{'id': obj.id} for obj in branches],
                'benefits': [{'id': obj.id} for obj in benefits],
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def company_step_4(execute):
    def closure(user, soft_skills, cultural_fits):
        return execute(company_profile_mutation(4), variables={
            'step4': {
                'softSkills': [{'id': obj.id} for obj in soft_skills],
                'culturalFits': [{'id': obj.id} for obj in cultural_fits],
            }
        }, **{'user': user})
    return closure
