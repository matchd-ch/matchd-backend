from datetime import datetime

import pytest

from graphql_relay import to_global_id

from db.models import JobPosting, JobPostingState

# pylint: disable=W0621
# pylint: disable=R0913
# pylint: disable=C0209


def job_posting_query(filter_value, param_name):
    if param_name == 'slug':
        param = f'slug: "{filter_value}"'
    else:
        param = f'id: {filter_value}'
    return '''
    query {
        jobPosting(%s) {
            dateCreated
            datePublished
            matchStatus {
              initiator
              confirmed
            }
            matchHints {
              hasRequestedMatch
              hasConfirmedMatch
            }
            id
            slug
            title
            displayTitle
            formStep
            state
            description
            jobType {
                id
                name
                mode
            }
            branches {
                id
                name
            }
            employee {
                id
                role
                firstName
                lastName
                email
            }
            company {
                id
            }
            workload
            jobFromDate
            jobToDate
            formStep
            url
            jobRequirements {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
            skills {
                id
                name
            }
            languages {
                language {
                    id
                    name
                }
                languageLevel {
                    id
                    description
                }
            }
        }
    }
    ''' % param


def job_posting_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on JobPosting {
                slug
            }
        }
    }
    '''


def job_postings_query(slug):
    return '''
    query {
        jobPostings(first: 2, slug: "%s") {
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    matchStatus {
                        initiator
                        confirmed
                    }
                    matchHints {
                        hasRequestedMatch
                        hasConfirmedMatch
                    }
                    id
                    slug
                    title
                    displayTitle
                    formStep
                    state
                    description
                    jobType {
                        id
                        name
                        mode
                    }
                    branches {
                        id
                        name
                    }
                    employee {
                        id
                        role
                        firstName
                        lastName
                        email
                    }
                    company {
                        id
                    }
                    workload
                    jobFromDate
                    jobToDate
                    formStep
                    url
                    jobRequirements {
                        edges {
                            node {
                                id
                                name
                            }
                        }
                    }
                    skills {
                        id
                        name
                    }
                    languages {
                        language {
                            id
                            name
                        }
                        languageLevel {
                            id
                            description
                        }
                    }
                }
            }
        }
    }
    ''' % slug


@pytest.fixture
def query_job_posting(execute):

    def closure(user, slug):
        return execute(job_posting_query(slug, 'slug'), **{'user': user})

    return closure


@pytest.fixture
def query_job_posting_by_id(execute):

    def closure(user, job_posting_id):
        return execute(job_posting_query(job_posting_id, 'id'), **{'user': user})

    return closure


@pytest.fixture
def query_job_posting_node(execute):

    def closure(user, id_value):
        return execute(job_posting_node_query(),
                       variables={'id': to_global_id('JobPosting', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_job_postings(execute):

    def closure(user, slug):
        return execute(job_postings_query(slug), **{'user': user})

    return closure


def job_posting_mutation(kind, gql_variable_name):
    return '''
    mutation JobPostingMutation($%s: JobPostingInput%s!) {
      jobPosting%s(%s: $%s) {
        success,
        errors,
        slug,
        jobPostingId
      }
    }
    ''' % (gql_variable_name, kind, kind, gql_variable_name, gql_variable_name)


@pytest.fixture
def job_posting_base_data(execute):

    def closure(user, title, description, job_type, branches, workload, job_from_date, job_to_date,
                url):
        return execute(job_posting_mutation("BaseData", "baseData"),
                       variables={
                           'baseData': {
                               'title': title,
                               'description': description,
                               'jobType': None if job_type is None else {
                                   'id': job_type.id
                               },
                               'branches': [{
                                   'id': obj.id
                               } for obj in branches],
                               'workload': workload,
                               'jobFromDate': job_from_date,
                               'jobToDate': job_to_date,
                               'url': url
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def job_posting_requirements(execute):

    def closure(user, job_posting_id, job_requirements, skills, languages):
        return execute(job_posting_mutation("Requirements", "requirements"),
                       variables={
                           'requirements': {
                               'id':
                               job_posting_id,
                               'jobRequirements': [{
                                   'id': obj.id
                               } for obj in job_requirements],
                               'skills': [{
                                   'id': obj.id
                               } for obj in skills],
                               'languages': [{
                                   'language': obj[0].id,
                                   'languageLevel': obj[1].id
                               } for obj in languages],
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def job_posting_allocation(execute):

    def closure(user, job_posting_id, state, employee):
        return execute(job_posting_mutation("Allocation", "allocation"),
                       variables={
                           'allocation': {
                               'id': job_posting_id,
                               'state': state,
                               'employee': {
                                   'id': employee.id
                               }
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def job_posting_objects(company_object, job_type_objects_date_range, branch_objects):
    job_posting_1 = JobPosting.objects.create(id=1,
                                              company=company_object,
                                              job_type=job_type_objects_date_range[0],
                                              job_from_date=datetime.now(),
                                              slug='job-1',
                                              state=JobPostingState.PUBLIC)
    job_posting_1.branches.set([branch_objects[0]])
    job_posting_2 = JobPosting.objects.create(id=2,
                                              company=company_object,
                                              job_type=job_type_objects_date_range[0],
                                              job_from_date=datetime.now(),
                                              slug='job-2',
                                              state=JobPostingState.PUBLIC)
    job_posting_2.branches.set([branch_objects[0]])
    job_posting_3 = JobPosting.objects.create(id=3,
                                              company=company_object,
                                              job_type=job_type_objects_date_range[0],
                                              job_from_date=datetime.now(),
                                              slug='job-3',
                                              state=JobPostingState.DRAFT)
    job_posting_3.branches.set([branch_objects[0]])
    return [
        job_posting_1,
        job_posting_2,
        job_posting_3,
    ]


@pytest.fixture
def job_posting_object(job_posting_objects):
    return job_posting_objects[0]


@pytest.fixture
def job_posting_object_2(job_posting_objects):
    return job_posting_objects[1]
