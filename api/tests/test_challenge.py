import pytest

from django.core import management
from django.contrib.auth.models import AnonymousUser

from graphql_relay import to_global_id

from api.tests.helper.node_helper import assert_node_field, assert_node_id

from db.models import Challenge, ChallengeState
# pylint: disable=R0913


@pytest.mark.django_db
def test_student_challenge(query_challenge, company_challenge_object: Challenge,
                           challenge_type_objects, keyword_objects, user_student, user_employee):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.team_size = 5
    company_challenge_object.compensation = 'to be discussed'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.state = ChallengeState.PUBLIC
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge(user_employee, company_challenge_object.slug)

    assert errors is None
    assert data is not None
    challenge = data.get('challenge')

    assert challenge.get('title') == 'title'
    assert challenge.get('displayTitle') == 'tit\xadle'
    assert challenge.get('slug') == company_challenge_object.slug
    assert challenge.get('description') == company_challenge_object.description
    assert challenge.get('teamSize') == company_challenge_object.team_size
    assert challenge.get('compensation') == company_challenge_object.compensation
    assert challenge.get('challengeFromDate') == '2021-08-01'
    assert challenge.get('website') == company_challenge_object.website
    assert challenge.get('challengeType').get('id') == to_global_id(
        'ChallengeType', company_challenge_object.challenge_type_id)
    assert int(challenge.get('formStep')) == company_challenge_object.form_step
    assert challenge.get('company') is None
    assert challenge.get('employee') is None
    assert challenge.get('student').get('id') == to_global_id('Student', user_student.student.id)
    assert len(challenge.get('keywords')) == len(company_challenge_object.keywords.all())
    assert challenge.get('state') == company_challenge_object.state.upper()

    match_status = challenge.get('matchStatus')
    assert match_status is None

    match_hints = challenge.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_student_challenge_draft(query_challenge, company_challenge_object: Challenge,
                                 challenge_type_objects, keyword_objects, user_student):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.team_size = 5
    company_challenge_object.compensation = 'to be discussed'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.state = ChallengeState.DRAFT
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge(user_student, company_challenge_object.slug)

    assert errors is None
    assert data is not None
    challenge = data.get('challenge')

    assert challenge.get('title') == 'title'
    assert challenge.get('displayTitle') == 'tit\xadle'
    assert challenge.get('slug') == company_challenge_object.slug
    assert challenge.get('description') == company_challenge_object.description
    assert challenge.get('teamSize') == company_challenge_object.team_size
    assert challenge.get('compensation') == company_challenge_object.compensation
    assert challenge.get('challengeFromDate') == '2021-08-01'
    assert challenge.get('website') == company_challenge_object.website
    assert challenge.get('challengeType').get('id') == to_global_id(
        'ChallengeType', company_challenge_object.challenge_type_id)
    assert int(challenge.get('formStep')) == company_challenge_object.form_step
    assert challenge.get('company') is None
    assert challenge.get('employee') is None
    assert challenge.get('student').get('id') == to_global_id('Student', user_student.student.id)
    assert len(challenge.get('keywords')) == len(company_challenge_object.keywords.all())
    assert challenge.get('state') == company_challenge_object.state.upper()

    match_status = challenge.get('matchStatus')
    assert match_status is None

    match_hints = challenge.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_student_challenge_by_id(query_challenge_by_id, company_challenge_object: Challenge,
                                 challenge_type_objects, keyword_objects, user_student):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.team_size = 5
    company_challenge_object.compensation = 'to be discussed'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.state = ChallengeState.PUBLIC
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge_by_id(user_student, company_challenge_object.id)

    assert errors is None
    assert data is not None
    challenge = data.get('challenge')

    assert challenge.get('title') == 'title'
    assert challenge.get('displayTitle') == 'tit\xadle'
    assert challenge.get('slug') == company_challenge_object.slug
    assert challenge.get('description') == company_challenge_object.description
    assert challenge.get('teamSize') == company_challenge_object.team_size
    assert challenge.get('compensation') == company_challenge_object.compensation
    assert challenge.get('challengeFromDate') == '2021-08-01'
    assert challenge.get('website') == company_challenge_object.website
    assert challenge.get('challengeType').get('id') == to_global_id(
        'ChallengeType', company_challenge_object.challenge_type_id)
    assert int(challenge.get('formStep')) == company_challenge_object.form_step
    assert challenge.get('company') is None
    assert challenge.get('employee') is None
    assert challenge.get('student').get('id') == to_global_id('Student', user_student.student.id)
    assert len(challenge.get('keywords')) == len(company_challenge_object.keywords.all())
    assert challenge.get('state') == company_challenge_object.state.upper()

    match_status = challenge.get('matchStatus')
    assert match_status is None

    match_hints = challenge.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_company_challenge(query_challenge, company_challenge_object: Challenge,
                           challenge_type_objects, keyword_objects, user_employee):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.team_size = 5
    company_challenge_object.compensation = 'to be discussed'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.student = None
    company_challenge_object.state = ChallengeState.PUBLIC
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge(user_employee, company_challenge_object.slug)

    assert errors is None
    assert data is not None
    challenge = data.get('challenge')

    assert challenge.get('title') == 'title'
    assert challenge.get('displayTitle') == 'tit\xadle'
    assert challenge.get('slug') == company_challenge_object.slug
    assert challenge.get('description') == company_challenge_object.description
    assert challenge.get('teamSize') == company_challenge_object.team_size
    assert challenge.get('compensation') == company_challenge_object.compensation
    assert challenge.get('challengeFromDate') == '2021-08-01'
    assert challenge.get('website') == company_challenge_object.website
    assert challenge.get('challengeType').get('id') == to_global_id(
        'ChallengeType', company_challenge_object.challenge_type_id)
    assert int(challenge.get('formStep')) == company_challenge_object.form_step
    assert challenge.get('company').get('id') == to_global_id('Company', user_employee.company.id)
    assert challenge.get('employee').get('id') == to_global_id('Employee',
                                                               user_employee.employee.id)
    assert challenge.get('student') is None
    assert len(challenge.get('keywords')) == len(company_challenge_object.keywords.all())
    assert challenge.get('state') == company_challenge_object.state.upper()

    match_status = challenge.get('matchStatus')
    assert match_status is None

    match_hints = challenge.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_company_challenge_draft(query_challenge, company_challenge_object: Challenge,
                                 challenge_type_objects, keyword_objects, user_employee):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.team_size = 5
    company_challenge_object.compensation = 'to be discussed'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.student = None
    company_challenge_object.state = ChallengeState.DRAFT
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge(user_employee, company_challenge_object.slug)

    assert errors is None
    assert data is not None
    challenge = data.get('challenge')

    assert challenge.get('title') == 'title'
    assert challenge.get('displayTitle') == 'tit\xadle'
    assert challenge.get('slug') == company_challenge_object.slug
    assert challenge.get('description') == company_challenge_object.description
    assert challenge.get('teamSize') == company_challenge_object.team_size
    assert challenge.get('compensation') == company_challenge_object.compensation
    assert challenge.get('challengeFromDate') == '2021-08-01'
    assert challenge.get('website') == company_challenge_object.website
    assert challenge.get('challengeType').get('id') == to_global_id(
        'ChallengeType', company_challenge_object.challenge_type_id)
    assert int(challenge.get('formStep')) == company_challenge_object.form_step
    assert challenge.get('company').get('id') == to_global_id('Company', user_employee.company.id)
    assert challenge.get('employee').get('id') == to_global_id('Employee',
                                                               user_employee.employee.id)
    assert challenge.get('student') is None
    assert len(challenge.get('keywords')) == len(company_challenge_object.keywords.all())
    assert challenge.get('state') == company_challenge_object.state.upper()

    match_status = challenge.get('matchStatus')
    assert match_status is None

    match_hints = challenge.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_company_challenge_by_id(query_challenge_by_id, company_challenge_object: Challenge,
                                 challenge_type_objects, keyword_objects, user_employee):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.team_size = 5
    company_challenge_object.compensation = 'to be discussed'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.student = None
    company_challenge_object.state = ChallengeState.PUBLIC
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge_by_id(user_employee, company_challenge_object.id)

    assert errors is None
    assert data is not None
    challenge = data.get('challenge')

    assert challenge.get('title') == 'title'
    assert challenge.get('displayTitle') == 'tit\xadle'
    assert challenge.get('slug') == company_challenge_object.slug
    assert challenge.get('description') == company_challenge_object.description
    assert challenge.get('teamSize') == company_challenge_object.team_size
    assert challenge.get('compensation') == company_challenge_object.compensation
    assert challenge.get('challengeFromDate') == '2021-08-01'
    assert challenge.get('website') == company_challenge_object.website
    assert challenge.get('challengeType').get('id') == to_global_id(
        'ChallengeType', company_challenge_object.challenge_type_id)
    assert int(challenge.get('formStep')) == company_challenge_object.form_step
    assert challenge.get('company').get('id') == to_global_id('Company', user_employee.company.id)
    assert challenge.get('employee').get('id') == to_global_id('Employee',
                                                               user_employee.employee.id)
    assert challenge.get('student') is None
    assert len(challenge.get('keywords')) == len(company_challenge_object.keywords.all())
    assert challenge.get('state') == company_challenge_object.state.upper()

    match_status = challenge.get('matchStatus')
    assert match_status is None

    match_hints = challenge.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_student_challenge_draft_not_accessible(query_challenge,
                                                company_challenge_object: Challenge,
                                                challenge_type_objects, keyword_objects,
                                                user_student, user_employee):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.state = ChallengeState.DRAFT
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge(user_employee, company_challenge_object.slug)

    assert errors is not None
    assert data is not None
    assert data.get('challenge') is None


@pytest.mark.django_db
def test_company_challenge_draft_not_accessible(query_challenge,
                                                company_challenge_object: Challenge,
                                                challenge_type_objects, keyword_objects,
                                                user_employee, user_student):
    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.student = None
    company_challenge_object.state = ChallengeState.DRAFT
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge(user_student, company_challenge_object.slug)

    assert errors is not None
    assert data is not None
    assert data.get('challenge') is None


@pytest.mark.django_db
def test_challenge_without_login(query_challenge, company_challenge_object: Challenge,
                                 challenge_type_objects, user_student, keyword_objects):

    company_challenge_object.title = 'title'
    company_challenge_object.slug = 'title'
    company_challenge_object.description = 'description'
    company_challenge_object.team_size = 5
    company_challenge_object.compensation = 'to be discussed'
    company_challenge_object.challenge_from_date = '2021-08-01'
    company_challenge_object.website = 'http://www.challenge-posting.lo'
    company_challenge_object.challenge_type = challenge_type_objects[0]
    company_challenge_object.form_step = 3
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.state = ChallengeState.PUBLIC
    company_challenge_object.save()
    company_challenge_object.keywords.set(keyword_objects)

    data, errors = query_challenge(AnonymousUser(), company_challenge_object.slug)

    assert errors is None
    assert data is not None
    challenge = data.get('challenge')

    assert challenge.get('title') == 'title'
    assert challenge.get('displayTitle') == 'tit\xadle'
    assert challenge.get('slug') == company_challenge_object.slug
    assert challenge.get('description') == company_challenge_object.description
    assert challenge.get('teamSize') is None
    assert challenge.get('compensation') is None
    assert challenge.get('challengeFromDate') == '2021-08-01'
    assert challenge.get('website') == ""
    assert challenge.get('challengeType').get('id') == to_global_id(
        'ChallengeType', company_challenge_object.challenge_type_id)
    assert int(challenge.get('formStep')) == 0
    assert challenge.get('company') is None
    assert challenge.get('employee') is None
    assert challenge.get('student') is None
    assert len(challenge.get('keywords')) == len(company_challenge_object.keywords.all())
    assert challenge.get('state') == company_challenge_object.state.upper()

    match_status = challenge.get('matchStatus')
    assert match_status is None

    match_hints = challenge.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_all_challenges_visible_to_anonymous(query_challenges, company_challenge_objects,
                                             student_challenge_objects):
    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == len(company_challenge_objects) + len(student_challenge_objects) - 2
    assert_node_id(edges[0].get('node'), 'Challenge', company_challenge_objects[0].id)
    assert_node_id(edges[1].get('node'), 'Challenge', company_challenge_objects[1].id)
    assert_node_field(edges[0].get('node'), 'slug', company_challenge_objects[0].slug)
    assert_node_field(edges[1].get('node'), 'slug', company_challenge_objects[1].slug)


@pytest.mark.django_db
def test_company_challenges_not_visible_to_company(query_challenges, company_challenge_objects,
                                                   user_employee):
    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(user_employee)
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 0


@pytest.mark.django_db
def test_student_challenges_visible_to_company(query_challenges, student_challenge_objects,
                                               user_employee):
    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(user_employee)
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == len(student_challenge_objects) - 1


@pytest.mark.django_db
def test_student_challenges_not_visible_to_student(query_challenges, student_challenge_objects,
                                                   user_student):
    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(user_student)
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == 0


@pytest.mark.django_db
def test_company_challenges_visible_to_student(query_challenges, company_challenge_objects,
                                               user_student):
    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(user_student)
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == len(company_challenge_objects) - 1


@pytest.mark.django_db
def test_node_query(query_challenge_node, company_challenge_objects, user_employee):
    data, errors = query_challenge_node(user_employee, company_challenge_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'Challenge', company_challenge_objects[0].id)
    assert_node_field(node, 'slug', company_challenge_objects[0].slug)


@pytest.mark.django_db
def test_challenges_without_login(query_challenges, company_challenge_objects):
    management.call_command('update_index', stdout=StringIO())

    data, errors = query_challenges(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('challenges').get('edges')
    assert edges is not None
    assert len(edges) == len(company_challenge_objects) - 1

    assert edges[0].get('node').get('team_size') is None
    assert edges[0].get('node').get('compensation') is None
    assert edges[0].get('node').get('website') == ""
    assert edges[0].get('node').get('employee') is None
    assert edges[0].get('node').get('student') is None
    assert edges[0].get('node').get('company') is None
    assert edges[0].get('node').get('match_status') is None
    assert edges[0].get('node').get('match_hints') is None
    assert int(edges[0].get('node').get('formStep')) == 0


@pytest.mark.django_db
def test_node_without_login(query_challenge_node, company_challenge_objects):
    data, errors = query_challenge_node(AnonymousUser(), company_challenge_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'Challenge', company_challenge_objects[0].id)
    assert_node_field(node, 'slug', company_challenge_objects[0].slug)
