import pytest

from db.models import ProfileState, Match


@pytest.mark.django_db
def test_student(login, user_student_full_profile, query_student, user_employee, branch_objects, job_type_objects,
                 skill_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()
    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') is None  # match protection
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('profileStep') == 3
    assert int(student.get('branch').get('id')) == branch_objects[0].id
    assert int(student.get('jobType').get('id')) == job_type_objects[0].id
    assert student.get('state') == ProfileState.PUBLIC.upper()
    assert student.get('mobile') is None  # match protection
    assert student.get('zip') is None  # match protection
    assert student.get('city') is None  # match protection
    assert student.get('street') is None  # match protection
    assert student.get('dateOfBirth') == '1337-03-01'
    assert student.get('nickname') == 'nickname'
    assert student.get('slug') == 'nickname'
    assert student.get('schoolName') == 'school name'
    assert student.get('fieldOfStudy') == 'field of study'
    assert student.get('graduation') == '1337-03-01'
    assert student.get('distinction') == 'distinction'
    assert len(student.get('skills')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineProjects')) == 2
    assert len(student.get('softSkills')) == 6
    assert len(student.get('culturalFits')) == 6

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_anonymous(login, user_student_full_profile, query_student, user_employee, branch_objects,
                           job_type_objects, skill_objects):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()
    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') is None
    assert student.get('firstName') is None
    assert student.get('lastName') is None
    assert student.get('profileStep') == 3
    assert int(student.get('branch').get('id')) == branch_objects[0].id
    assert int(student.get('jobType').get('id')) == job_type_objects[0].id
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
    assert len(student.get('skills')) == len(skill_objects)
    assert student.get('hobbies') is None
    assert student.get('onlineProjects') is None
    assert len(student.get('softSkills')) == 6
    assert len(student.get('culturalFits')) == 6

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_anonymous_with_match_initiated_by_student(login, user_student_full_profile, query_student,
                                                           user_employee, branch_objects, job_type_objects,
                                                           skill_objects, job_posting_object):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(job_posting=job_posting_object, student=user_student_full_profile.student,
                                 initiator=user_student_full_profile.type, student_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('profileStep') == 3
    assert int(student.get('branch').get('id')) == branch_objects[0].id
    assert int(student.get('jobType').get('id')) == job_type_objects[0].id
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
    assert len(student.get('skills')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineProjects')) == 2
    assert len(student.get('softSkills')) == 6
    assert len(student.get('culturalFits')) == 6

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_anonymous_with_match_initiated_by_employee_but_not_confirmed(
        login, user_student_full_profile, query_student, user_employee, branch_objects, job_type_objects, skill_objects,
        job_posting_object):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(job_posting=job_posting_object, student=user_student_full_profile.student,
                                 initiator=user_employee.type, company_confirmed=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') is None
    assert student.get('firstName') is None
    assert student.get('lastName') is None
    assert student.get('profileStep') == 3
    assert int(student.get('branch').get('id')) == branch_objects[0].id
    assert int(student.get('jobType').get('id')) == job_type_objects[0].id
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
    assert len(student.get('skills')) == len(skill_objects)
    assert student.get('hobbies') is None
    assert student.get('onlineProjects') is None
    assert len(student.get('softSkills')) == 6
    assert len(student.get('culturalFits')) == 6

    company = student.get('company')
    assert company is None


@pytest.mark.django_db
def test_student_anonymous_with_match_initiated_by_employee_and_confirmed(
        login, user_student_full_profile, query_student, user_employee, branch_objects, job_type_objects, skill_objects,
        job_posting_object):
    user_student_full_profile.student.state = ProfileState.ANONYMOUS
    user_student_full_profile.student.save()

    Match.objects.create(job_posting=job_posting_object, student=user_student_full_profile.student,
                                 initiator=user_employee.type, company_confirmed=True, student_confirmed=True, complete=True)

    login(user_employee)
    data, errors = query_student(user_employee, user_student_full_profile.student.slug)

    student = data.get('student')
    assert student is not None
    assert student.get('email') == 'student@matchd.test'
    assert student.get('firstName') == 'John'
    assert student.get('lastName') == 'Doe'
    assert student.get('profileStep') == 3
    assert int(student.get('branch').get('id')) == branch_objects[0].id
    assert int(student.get('jobType').get('id')) == job_type_objects[0].id
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
    assert len(student.get('skills')) == len(skill_objects)
    assert len(student.get('hobbies')) == 2
    assert len(student.get('onlineProjects')) == 2
    assert len(student.get('softSkills')) == 6
    assert len(student.get('culturalFits')) == 6

    company = student.get('company')
    assert company is None
