import pytest

from graphql_relay import to_global_id

from db.models import Challenge, ChallengeState

# pylint: disable=C0209


def challenge_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Challenge {
                slug
            }
        }
    }
    '''


def challenge_query(filter_value, param_name):
    if param_name == 'slug':
        param = f'slug: "{filter_value}"'
    else:
        param = f'id: "{filter_value}"'
    return '''
    query {
        challenge(%s) {
            avatarUrl
            dateCreated
            datePublished
            id
            slug
            title
            displayTitle
            description
            teamSize
            compensation
            challengeType {
              id
              name
            }
            keywords {
              id
              name
            }
            website
            challengeFromDate
            formStep
            state
            company {
              id
            }
            student {
              slug
              id
            }
            employee {
              email
              id
            }
            matchStatus {
              confirmed
              initiator
            }
            matchHints {
              hasRequestedMatch
              hasConfirmedMatch
            }
        }
    }
    ''' % param


def challenges_query(filters=None):
    return '''
    query {
        challenges(first: 10%s) {
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    avatarUrl
                    dateCreated
                    datePublished
                    id
                    slug
                    title
                    displayTitle
                    description
                    teamSize
                    compensation
                    challengeType {
                        id
                        name
                    }
                    keywords {
                        id
                        name
                    }
                    website
                    challengeFromDate
                    formStep
                    state
                    company {
                        id
                    }
                    student {
                        slug
                        id
                    }
                    employee {
                        email
                        id
                    }
                    matchStatus {
                        confirmed
                        initiator
                    }
                    matchHints {
                        hasRequestedMatch
                        hasConfirmedMatch
                    }
                }
            }
        }
    }
    ''' % stringify_filters(filters)


@pytest.fixture
def query_challenge(execute):

    def closure(user, slug):
        return execute(challenge_query(slug, 'slug'), **{'user': user})

    return closure


@pytest.fixture
def query_challenge_by_id(execute):

    def closure(user, challenge_id):
        return execute(challenge_query(to_global_id('Challenge', challenge_id), 'id'),
                       **{'user': user})

    return closure


@pytest.fixture
def query_challenge_node(execute):

    def closure(user, id_value):
        return execute(challenge_node_query(),
                       variables={'id': to_global_id('Challenge', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_challenges(execute):

    def closure(user, filters=None):
        return execute(challenges_query(filters), **{'user': user})

    return closure


@pytest.fixture
def company_challenge_objects(company_object_complete, challenge_type_objects):
    challenge_1 = Challenge.objects.create(id=1,
                                           title="challenge1",
                                           description="one",
                                           company=company_object_complete,
                                           slug='challenge-1',
                                           challenge_type=challenge_type_objects[0],
                                           state=ChallengeState.PUBLIC,
                                           team_size=1)
    challenge_2 = Challenge.objects.create(id=2,
                                           title="challenge2",
                                           description="two",
                                           company=company_object_complete,
                                           slug='challenge-2',
                                           challenge_type=challenge_type_objects[0],
                                           state=ChallengeState.PUBLIC,
                                           team_size=1)
    challenge_3 = Challenge.objects.create(id=3,
                                           title="challenge3",
                                           description="three",
                                           company=company_object_complete,
                                           slug='challenge-3',
                                           challenge_type=challenge_type_objects[0],
                                           state=ChallengeState.DRAFT,
                                           team_size=1)
    challenge_4 = Challenge.objects.create(id=4,
                                           title="challenge4",
                                           description="four",
                                           company=company_object_complete,
                                           slug='challenge-4',
                                           challenge_type=challenge_type_objects[1],
                                           state=ChallengeState.PUBLIC,
                                           team_size=10)
    challenge_5 = Challenge.objects.create(id=5,
                                           title="challenge5",
                                           description="five",
                                           company=company_object_complete,
                                           slug='challenge-5',
                                           challenge_type=challenge_type_objects[2],
                                           state=ChallengeState.PUBLIC,
                                           team_size=5)
    return [
        challenge_1,
        challenge_2,
        challenge_3,
        challenge_4,
        challenge_5,
    ]


@pytest.fixture
def student_challenge_objects(user_student_full_profile, challenge_type_objects):
    challenge_1 = Challenge.objects.create(id=6,
                                           student=user_student_full_profile.student,
                                           slug='student-challenge-1',
                                           challenge_type=challenge_type_objects[0],
                                           state=ChallengeState.PUBLIC,
                                           team_size=1)
    challenge_2 = Challenge.objects.create(id=7,
                                           student=user_student_full_profile.student,
                                           slug='student-challenge-2',
                                           challenge_type=challenge_type_objects[0],
                                           state=ChallengeState.PUBLIC,
                                           team_size=1)
    challenge_3 = Challenge.objects.create(id=8,
                                           student=user_student_full_profile.student,
                                           slug='student-challenge-3',
                                           challenge_type=challenge_type_objects[0],
                                           state=ChallengeState.DRAFT,
                                           team_size=1)
    challenge_4 = Challenge.objects.create(id=9,
                                           student=user_student_full_profile.student,
                                           slug='student-challenge-4',
                                           challenge_type=challenge_type_objects[1],
                                           state=ChallengeState.PUBLIC,
                                           team_size=1)
    return [
        challenge_1,
        challenge_2,
        challenge_3,
        challenge_4,
    ]


# pylint: disable=W0621
@pytest.fixture
def company_challenge_object(company_challenge_objects):
    return company_challenge_objects[0]


# pylint: disable=W0621
@pytest.fixture
def student_challenge_object(student_challenge_objects):
    return student_challenge_objects[0]


def challenge_mutation(kind):
    return '''
    mutation ChallengeMutation($input: Challenge%sInput!) {
      challenge%s(input: $input) {
        success,
        errors,
        slug,
        challengeId
      }
    }
    ''' % (kind, kind)


def delete_challenge_mutation():
    return '''
    mutation DeleteChallenge($input: DeleteChallengeInput!) {
      deleteChallenge(input: $input) {
        success,
        errors
      }
    }
    '''


@pytest.fixture
def delete_challenge(execute):

    def closure(user, challenge_id):
        return execute(delete_challenge_mutation(),
                       variables={'input': {
                           'id': to_global_id('Challenge', challenge_id),
                       }},
                       **{'user': user})

    return closure


# pylint: disable=R0913
@pytest.fixture
def challenge_base_data(execute):

    def closure(user, title, description, team_size, compensation, challenge_type, keywords):
        return execute(challenge_mutation("BaseData"),
                       variables={
                           'input': {
                               'id':
                               None,
                               'title':
                               title,
                               'description':
                               description,
                               'teamSize':
                               team_size,
                               'compensation':
                               compensation,
                               'challengeType':
                               None if challenge_type is None else {
                                   'id': to_global_id('ChallengeType', challenge_type.id)
                               },
                               'keywords': [{
                                   'id': to_global_id('Keywords', obj.id)
                               } for obj in keywords]
                           }
                       },
                       **{'user': user})

    return closure


# pylint: disable=R0913
@pytest.fixture
def challenge_specific_data(execute):

    def closure(user, challenge_id, challenge_from_date, website):
        return execute(challenge_mutation("SpecificData"),
                       variables={
                           'input': {
                               'id': to_global_id('Challenge', challenge_id),
                               'challengeFromDate': challenge_from_date,
                               'website': website,
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def challenge_allocation(execute):

    def closure(user, challenge_id, state, employee):
        return execute(challenge_mutation("Allocation"),
                       variables={
                           'input': {
                               'id': to_global_id('Challenge', challenge_id),
                               'state': state,
                               'employee': None if employee is None else {
                                   'id': to_global_id('Employee', employee.id)
                               }
                           }
                       },
                       **{'user': user})

    return closure


def stringify_filters(filters):
    string = ""

    if filters is None:
        return string

    for key, value in filters.items():
        string += f", {key}: {value}"
    return string.replace("\'", "")
