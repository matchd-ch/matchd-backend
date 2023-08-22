import pytest

from graphql_relay import to_global_id

from db.models import ProfileState, Match

# pylint: disable=R0913
# pylint: disable=W0612


@pytest.mark.django_db
def test_student(login, user_student_full_profile, query_student, user_employee, branch_objects,
                 job_type_objects, skill_objects, student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    for challenge in student_challenge_objects:
        challenge.student = user_student_full_profile.student
        challenge.save()

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)
    assert errors is None

    student = data.get('student')
    assert student is not None

    assert student.get('email') is None    # match protection
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.PUBLIC.upper()
    assert student.get('mobile') is None    # match protection
    assert student.get('zip') is None    # match protection
    assert student.get('city') is None    # match protection
    assert student.get('street') is None    # match protection
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineChallenges')) == 2
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert len(student.get('challenges')) == 3    # public only
    assert student.get('matchStatus') is None

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_profile_100_percent_complete(login, user_student_full_profile, query_student,
                                              user_employee, branch_objects,
                                              student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    for challenge in student_challenge_objects:
        challenge.student = user_student_full_profile.student
        challenge.save()

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)
    assert errors is None

    student = data.get('student')
    assert student is not None


@pytest.mark.django_db
def test_student_profile_0_percent_complete(login, user_student_full_profile, query_student,
                                            user_employee, branch_objects,
                                            student_challenge_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.street = ''
    user_student_full_profile.student.zip = ''
    user_student_full_profile.student.city = ''
    user_student_full_profile.student.date_of_birth = None
    user_student_full_profile.student.school_name = ''
    user_student_full_profile.student.field_of_study = ''
    user_student_full_profile.student.graduation = None
    user_student_full_profile.student.branch = None
    user_student_full_profile.student.distinction = ''
    user_student_full_profile.student.skills.set([])
    user_student_full_profile.student.soft_skills.set([])
    user_student_full_profile.student.cultural_fits.set([])
    user_student_full_profile.student.save()

    for challenge in student_challenge_objects:
        challenge.student = user_student_full_profile.student
        challenge.save()

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)
    assert errors is None

    student = data.get('student')
    assert student is not None


@pytest.mark.django_db
def test_student_anonymous(login, user_student_full_profile, query_student, user_employee,
                           branch_objects, job_type_objects, skill_objects):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()
    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') is None
    assert student.get('firstName') is None
    assert student.get('lastName') is None
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') is None
    assert student.get('zip') is None
    assert student.get('city') is None
    assert student.get('street') is None
    assert student.get('dateOfBirth') is None
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') is None
    assert student.get('fieldOfStudy') is None
    assert student.get('graduation') is None
    assert student.get('distinction') is None
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert student.get('hobbies') is None
    assert student.get('onlineChallenges') is None
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_anonymous_with_match_initiated_by_student(login, user_student_full_profile,
                                                           query_student, user_employee,
                                                           branch_objects, job_type_objects,
                                                           skill_objects, job_posting_object):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(job_posting=job_posting_object,
                         student=user_student_full_profile.student,
                         initiator=user_student_full_profile.type,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineChallenges')) == 2
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_anonymous_with_match_initiated_by_employee_but_not_confirmed(
        login, user_student_full_profile, query_student, user_employee, branch_objects,
        job_type_objects, skill_objects, job_posting_object):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(job_posting=job_posting_object,
                         student=user_student_full_profile.student,
                         initiator=user_employee.type,
                         company_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') is None
    assert student.get('firstName') is None
    assert student.get('lastName') is None
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') is None
    assert student.get('zip') is None
    assert student.get('city') is None
    assert student.get('street') is None
    assert student.get('dateOfBirth') is None
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') is None
    assert student.get('fieldOfStudy') is None
    assert student.get('graduation') is None
    assert student.get('distinction') is None
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert student.get('hobbies') is None
    assert student.get('onlineChallenges') is None
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_anonymous_with_match_initiated_by_employee_and_confirmed(
        login, user_student_full_profile, query_student, user_employee, branch_objects,
        job_type_objects, skill_objects, job_posting_object):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(job_posting=job_posting_object,
                         student=user_student_full_profile.student,
                         initiator=user_employee.type,
                         company_confirmed=True,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineChallenges')) == 2
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_with_match_status_initiated_from_student(login, user_student_full_profile,
                                                          query_student, user_employee,
                                                          job_posting_object):
    Match.objects.create(job_posting=job_posting_object,
                         student=user_student_full_profile.student,
                         initiator=user_student_full_profile.type,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug,
                                 job_posting_object.id)

    student = data.get('student')
    match_status = student.get('matchStatus')
    assert match_status is not None
    assert match_status.get('initiator') == user_student_full_profile.type.upper()
    assert match_status.get('confirmed') is False


@pytest.mark.django_db
def test_student_with_match_status_initiated_from_employee(login, user_student_full_profile,
                                                           query_student, user_employee,
                                                           job_posting_object):
    Match.objects.create(job_posting=job_posting_object,
                         student=user_student_full_profile.student,
                         initiator=user_employee.type,
                         company_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug,
                                 job_posting_object.id)

    student = data.get('student')
    match_status = student.get('matchStatus')
    assert match_status is not None
    assert match_status.get('initiator') == user_employee.type.upper()
    assert match_status.get('confirmed') is False


@pytest.mark.django_db
def test_student_with_confirmed_match_status(login, user_student_full_profile, query_student,
                                             user_employee, job_posting_object):
    Match.objects.create(job_posting=job_posting_object,
                         student=user_student_full_profile.student,
                         initiator=user_employee.type,
                         company_confirmed=True,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug,
                                 job_posting_object.id)
    assert data is not None
    assert errors is None

    student = data.get('student')
    match_status = student.get('matchStatus')
    assert match_status is not None
    assert match_status.get('initiator') == user_employee.type.upper()
    assert match_status.get('confirmed') is True


@pytest.mark.django_db
def test_student_with_confirmed_challenge_company_initiated(login, user_student_full_profile,
                                                            query_student, user_employee,
                                                            student_challenge_object,
                                                            branch_objects, skill_objects,
                                                            job_type_objects):
    Match.objects.create(company=user_employee.company,
                         challenge=student_challenge_object,
                         initiator=user_employee.type,
                         company_confirmed=True,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)
    assert data is not None
    assert errors is None

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.PUBLIC.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineChallenges')) == 2
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None


@pytest.mark.django_db
def test_anonymous_student_with_confirmed_challenge_company_initiated(
        login, user_student_full_profile, query_student, user_employee, student_challenge_object,
        branch_objects, skill_objects, job_type_objects):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(company=user_employee.company,
                         challenge=student_challenge_object,
                         initiator=user_employee.type,
                         company_confirmed=True,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)
    assert data is not None
    assert errors is None

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineChallenges')) == 2
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None


@pytest.mark.django_db
def test_student_with_confirmed_challenge_student_initiated(login, user_student_full_profile,
                                                            query_student, user_employee,
                                                            company_challenge_object,
                                                            branch_objects, skill_objects,
                                                            job_type_objects):
    Match.objects.create(student=user_student_full_profile.student,
                         challenge=company_challenge_object,
                         initiator=user_student_full_profile.type,
                         company_confirmed=True,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)
    assert data is not None
    assert errors is None

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.PUBLIC.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineChallenges')) == 2
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None


@pytest.mark.django_db
def test_anonymous_student_with_confirmed_challenge_student_initiated(
        login, user_student_full_profile, query_student, user_employee, company_challenge_object,
        branch_objects, skill_objects, job_type_objects):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(student=user_student_full_profile.student,
                         challenge=company_challenge_object,
                         initiator=user_student_full_profile.type,
                         company_confirmed=True,
                         student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)
    assert data is not None
    assert errors is None

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('branch').get('id') == to_global_id('Branch', branch_objects[0].id)
    assert student.get('jobType').get('id') == to_global_id('JobType', job_type_objects[0].id)
    assert student.get('state') == ProfileState.ANONYMOUS.upper()
    assert student.get('mobile') == '+41711234567'
    assert student.get('zip') == '1337'
    assert student.get('city') == 'nowhere'
    assert student.get('street') == 'street 1337'
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills').get('edges')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineChallenges')) == 2
    assert len(student.get('softSkills').get('edges')) == 6
    assert len(student.get('culturalFits').get('edges')) == 6
    assert student.get('matchStatus') is None


@pytest.mark.django_db
def test_update_student(login, user_student_full_profile, update_student):
    login(user_student_full_profile)

    is_matchable = False

    student_data = {"isMatchable": is_matchable}

    data, errors = update_student(user_student_full_profile, student_data)
    assert data is not None
    assert errors is None
    assert data.get('updateStudent').get('success')
    assert data.get('updateStudent').get('errors') is None

    assert data.get('updateStudent').get('student').get('isMatchable') == is_matchable
