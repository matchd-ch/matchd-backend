import pytest

# pylint: disable=R0913
# pylint: disable=C0209


def university_profile_mutation(step):
    step = str(step)
    return '''
    mutation UniversityProfileMutation($step%s: UniversityProfileInputStep%s!) {
        universityProfileStep%s(step%s: $step%s) {
            success,
            errors
        }
    }
    ''' % (step, step, step, step, step)


@pytest.fixture
def university_step_1(execute):
    def closure(user, first_name, last_name, name, street, zip_value, city, phone, role, website,
                top_level_organisation_website, top_level_organisation_description):
        return execute(university_profile_mutation(1), variables={
            'step1': {
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
        }, **{'user': user})
    return closure


@pytest.fixture
def university_step_2(execute):
    def closure(user, description):
        return execute(university_profile_mutation(2), variables={
            'step2': {
                'description': description,
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def university_step_3(execute):
    def closure(user, services, link_education, link_projects, link_thesis, branches, benefits):
        return execute(university_profile_mutation(3), variables={
            'step3': {
                'services': services,
                'linkEducation': link_education,
                'linkProjects': link_projects,
                'linkThesis': link_thesis,
                'branches': [{'id': obj.id} for obj in branches],
                'benefits': [{'id': obj.id} for obj in benefits],
            }
        }, **{'user': user})
    return closure

@pytest.fixture
def university_step_4(execute):
    def closure(user, soft_skills, cultural_fits):
        return execute(university_profile_mutation(4), variables={
            'step4': {
                'softSkills': [{'id': obj.id} for obj in soft_skills],
                'culturalFits': [{'id': obj.id} for obj in cultural_fits],
            }
        }, **{'user': user})
    return closure
