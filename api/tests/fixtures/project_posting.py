import pytest

from graphql_relay import to_global_id

from db.models import ProjectPosting, ProjectPostingState

# pylint: disable=C0209


def project_posting_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on ProjectPosting {
                slug
            }
        }
    }
    '''


def project_posting_query(filter_value, param_name):
    if param_name == 'slug':
        param = f'slug: "{filter_value}"'
    else:
        param = f'id: {filter_value}'
    return '''
    query {
        projectPosting(%s) {
            dateCreated
            datePublished
            id
            slug
            title
            displayTitle
            description
            additionalInformation
            topic {
              id
              name
            }
            projectType {
              id
              name
            }
            keywords {
              id
              name
            }
            website
            projectFromDate
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


def project_postings_query():
    return '''
    query {
        projectPostings(first: 3) {
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    dateCreated
                    datePublished
                    id
                    slug
                    title
                    displayTitle
                    description
                    additionalInformation
                    topic {
                        id
                        name
                    }
                    projectType {
                        id
                        name
                    }
                    keywords {
                        id
                        name
                    }
                    website
                    projectFromDate
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
    '''


@pytest.fixture
def query_project_posting(execute):

    def closure(user, slug):
        return execute(project_posting_query(slug, 'slug'), **{'user': user})

    return closure


@pytest.fixture
def query_project_posting_by_id(execute):

    def closure(user, project_posting_id):
        return execute(project_posting_query(project_posting_id, 'id'), **{'user': user})

    return closure


@pytest.fixture
def query_project_posting_node(execute):

    def closure(user, id_value):
        return execute(project_posting_node_query(),
                       variables={'id': to_global_id('ProjectPosting', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_project_postings(execute):

    def closure(user):
        return execute(project_postings_query(), **{'user': user})

    return closure


@pytest.fixture
def company_project_posting_objects(company_object, project_type_objects, topic_objects):
    project_posting_1 = ProjectPosting.objects.create(id=1,
                                                      company=company_object,
                                                      slug='project-1',
                                                      project_type=project_type_objects[0],
                                                      topic=topic_objects[0],
                                                      state=ProjectPostingState.PUBLIC)
    project_posting_2 = ProjectPosting.objects.create(id=2,
                                                      company=company_object,
                                                      slug='project-2',
                                                      project_type=project_type_objects[0],
                                                      topic=topic_objects[0],
                                                      state=ProjectPostingState.PUBLIC)
    project_posting_3 = ProjectPosting.objects.create(id=3,
                                                      company=company_object,
                                                      slug='project-3',
                                                      project_type=project_type_objects[0],
                                                      topic=topic_objects[0],
                                                      state=ProjectPostingState.DRAFT)
    return [
        project_posting_1,
        project_posting_2,
        project_posting_3,
    ]


@pytest.fixture
def student_project_posting_objects(user_student, project_type_objects, topic_objects):
    project_posting_1 = ProjectPosting.objects.create(id=4,
                                                      student=user_student.student,
                                                      slug='student-project-1',
                                                      project_type=project_type_objects[0],
                                                      topic=topic_objects[0],
                                                      state=ProjectPostingState.PUBLIC)
    project_posting_2 = ProjectPosting.objects.create(id=5,
                                                      student=user_student.student,
                                                      slug='student-project-2',
                                                      project_type=project_type_objects[0],
                                                      topic=topic_objects[0],
                                                      state=ProjectPostingState.PUBLIC)
    project_posting_3 = ProjectPosting.objects.create(id=6,
                                                      student=user_student.student,
                                                      slug='student-project-3',
                                                      project_type=project_type_objects[0],
                                                      topic=topic_objects[0],
                                                      state=ProjectPostingState.DRAFT)
    return [
        project_posting_1,
        project_posting_2,
        project_posting_3,
    ]


# pylint: disable=W0621
@pytest.fixture
def company_project_posting_object(company_project_posting_objects):
    return company_project_posting_objects[0]


# pylint: disable=W0621
@pytest.fixture
def student_project_posting_object(student_project_posting_objects):
    return student_project_posting_objects[0]


def project_posting_mutation(step):
    step = str(step)
    return '''
    mutation ProjectPostingMutation($step%s: ProjectPostingInputStep%s!) {
      projectPostingStep%s(step%s: $step%s) {
        success,
        errors,
        slug,
        projectPostingId
      }
    }
    ''' % (step, step, step, step, step)


# pylint: disable=R0913
@pytest.fixture
def project_posting_step_1(execute):

    def closure(user, title, description, additional_information, topic, project_type, keywords):
        return execute(project_posting_mutation(1),
                       variables={
                           'step1': {
                               'title': title,
                               'description': description,
                               'additionalInformation': additional_information,
                               'topic': None if topic is None else {
                                   'id': topic.id
                               },
                               'projectType': None if project_type is None else {
                                   'id': project_type.id
                               },
                               'keywords': [{
                                   'id': obj.id
                               } for obj in keywords]
                           }
                       },
                       **{'user': user})

    return closure


# pylint: disable=R0913
@pytest.fixture
def project_posting_step_2(execute):

    def closure(user, project_posting_id, project_from_date, website):
        return execute(project_posting_mutation(2),
                       variables={
                           'step2': {
                               'id': project_posting_id,
                               'projectFromDate': project_from_date,
                               'website': website,
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def project_posting_step_3(execute):

    def closure(user, project_posting_id, state, employee):
        return execute(project_posting_mutation(3),
                       variables={
                           'step3': {
                               'id': project_posting_id,
                               'state': state,
                               'employee': None if employee is None else {
                                   'id': employee.id
                               }
                           }
                       },
                       **{'user': user})

    return closure
