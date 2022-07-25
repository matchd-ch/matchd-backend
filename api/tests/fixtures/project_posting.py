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
        param = f'id: "{filter_value}"'
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
            teamSize
            compensation
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
        }
    }
    ''' % param


def project_postings_query(filters=None):
    return '''
    query {
        projectPostings(first: 10%s) {
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
                    teamSize
                    compensation
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
                }
            }
        }
    }
    ''' % stringify_filters(filters)


@pytest.fixture
def query_project_posting(execute):

    def closure(user, slug):
        return execute(project_posting_query(slug, 'slug'), **{'user': user})

    return closure


@pytest.fixture
def query_project_posting_by_id(execute):

    def closure(user, project_posting_id):
        return execute(
            project_posting_query(to_global_id('ProjectPosting', project_posting_id), 'id'),
            **{'user': user})

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

    def closure(user, filters=None):
        return execute(project_postings_query(filters), **{'user': user})

    return closure


@pytest.fixture
def company_project_posting_objects(company_object_complete, project_type_objects):
    project_posting_1 = ProjectPosting.objects.create(id=1,
                                                      company=company_object_complete,
                                                      slug='project-1',
                                                      project_type=project_type_objects[0],
                                                      state=ProjectPostingState.PUBLIC,
                                                      team_size=1)
    project_posting_2 = ProjectPosting.objects.create(id=2,
                                                      company=company_object_complete,
                                                      slug='project-2',
                                                      project_type=project_type_objects[0],
                                                      state=ProjectPostingState.PUBLIC,
                                                      team_size=1)
    project_posting_3 = ProjectPosting.objects.create(id=3,
                                                      company=company_object_complete,
                                                      slug='project-3',
                                                      project_type=project_type_objects[0],
                                                      state=ProjectPostingState.DRAFT,
                                                      team_size=1)
    project_posting_4 = ProjectPosting.objects.create(id=4,
                                                      company=company_object_complete,
                                                      slug='project-4',
                                                      project_type=project_type_objects[1],
                                                      state=ProjectPostingState.PUBLIC,
                                                      team_size=10)
    project_posting_5 = ProjectPosting.objects.create(id=5,
                                                      company=company_object_complete,
                                                      slug='project-5',
                                                      project_type=project_type_objects[1],
                                                      state=ProjectPostingState.PUBLIC,
                                                      team_size=5)
    return [
        project_posting_1,
        project_posting_2,
        project_posting_3,
        project_posting_4,
        project_posting_5,
    ]


@pytest.fixture
def student_project_posting_objects(user_student_full_profile, project_type_objects):
    project_posting_1 = ProjectPosting.objects.create(id=6,
                                                      student=user_student_full_profile.student,
                                                      slug='student-project-1',
                                                      project_type=project_type_objects[0],
                                                      state=ProjectPostingState.PUBLIC,
                                                      team_size=1)
    project_posting_2 = ProjectPosting.objects.create(id=7,
                                                      student=user_student_full_profile.student,
                                                      slug='student-project-2',
                                                      project_type=project_type_objects[0],
                                                      state=ProjectPostingState.PUBLIC,
                                                      team_size=1)
    project_posting_3 = ProjectPosting.objects.create(id=8,
                                                      student=user_student_full_profile.student,
                                                      slug='student-project-3',
                                                      project_type=project_type_objects[0],
                                                      state=ProjectPostingState.DRAFT,
                                                      team_size=1)
    project_posting_4 = ProjectPosting.objects.create(id=9,
                                                      student=user_student_full_profile.student,
                                                      slug='student-project-4',
                                                      project_type=project_type_objects[1],
                                                      state=ProjectPostingState.PUBLIC,
                                                      team_size=1)
    return [
        project_posting_1,
        project_posting_2,
        project_posting_3,
        project_posting_4,
    ]


# pylint: disable=W0621
@pytest.fixture
def company_project_posting_object(company_project_posting_objects):
    return company_project_posting_objects[0]


# pylint: disable=W0621
@pytest.fixture
def student_project_posting_object(student_project_posting_objects):
    return student_project_posting_objects[0]


def project_posting_mutation(kind):
    return '''
    mutation ProjectPostingMutation($input: ProjectPosting%sInput!) {
      projectPosting%s(input: $input) {
        success,
        errors,
        slug,
        projectPostingId
      }
    }
    ''' % (kind, kind)


# pylint: disable=R0913
@pytest.fixture
def project_posting_base_data(execute):

    def closure(user, title, description, team_size, compensation, project_type, keywords):
        return execute(project_posting_mutation("BaseData"),
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
                               'projectType':
                               None if project_type is None else {
                                   'id': to_global_id('ProjectType', project_type.id)
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
def project_posting_specific_data(execute):

    def closure(user, project_posting_id, project_from_date, website):
        return execute(project_posting_mutation("SpecificData"),
                       variables={
                           'input': {
                               'id': to_global_id('ProjectPosting', project_posting_id),
                               'projectFromDate': project_from_date,
                               'website': website,
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def project_posting_allocation(execute):

    def closure(user, project_posting_id, state, employee):
        return execute(project_posting_mutation("Allocation"),
                       variables={
                           'input': {
                               'id': to_global_id('ProjectPosting', project_posting_id),
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
