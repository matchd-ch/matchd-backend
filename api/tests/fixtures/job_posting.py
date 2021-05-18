from datetime import datetime
import pytest

from db.models import JobPosting

# pylint: disable=W0621
# pylint: disable=R0913


def job_posting_query(filter_value, param_name):
    if param_name == 'slug':
        param = 'slug: "%s"' % filter_value
    else:
        param = 'id: %s' % filter_value
    return '''
    query {
        jobPosting(%s) {
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
                id
                name
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


def job_postings_query(slug):
    return '''
    query {
        jobPostings(slug: "%s") {
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
                id
                name
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
def query_job_postings(execute):
    def closure(user, slug):
        return execute(job_postings_query(slug), **{'user': user})
    return closure


def job_posting_mutation(step):
    step = str(step)
    return '''
    mutation JobPostingMutation($step%s: JobPostingInputStep%s!) {
      jobPostingStep%s(step%s: $step%s) {
        success,
        errors,
        slug,
        jobPostingId
      }
    }
    ''' % (step, step, step, step, step)


@pytest.fixture
def job_posting_step_1(execute):
    def closure(user, title, description, job_type, branches, workload, job_from_date, job_to_date, url):
        return execute(job_posting_mutation(1), variables={
            'step1': {
                'title': title,
                'description': description,
                'jobType': None if job_type is None else {'id': job_type.id},
                'branches': [{'id': obj.id} for obj in branches],
                'workload': workload,
                'jobFromDate': job_from_date,
                'jobToDate': job_to_date,
                'url': url
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def job_posting_step_2(execute):
    def closure(user, job_posting_id, job_requirements, skills, languages):
        return execute(job_posting_mutation(2), variables={
            'step2': {
                'id': job_posting_id,
                'jobRequirements': [{'id': obj.id} for obj in job_requirements],
                'skills': [{'id': obj.id} for obj in skills],
                'languages': [
                    {'language': obj[0].id, 'languageLevel': obj[1].id}
                    for obj in languages
                ],
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def job_posting_step_3(execute):
    def closure(user, job_posting_id, state, employee):
        return execute(job_posting_mutation(3), variables={
            'step3': {
                'id': job_posting_id,
                'state': state,
                'employee': {'id': employee.id}
            }
        }, **{'user': user})
    return closure


@pytest.fixture
def job_posting_objects(company_object, job_type_objects_date_range, branch_objects):
    job_posting_1 = JobPosting.objects.create(id=1, company=company_object, job_type=job_type_objects_date_range[0],
                                              job_from_date=datetime.now(), slug='job-1')
    job_posting_1.branches.set([branch_objects[0]])
    job_posting_2 = JobPosting.objects.create(id=2, company=company_object, job_type=job_type_objects_date_range[0],
                                              job_from_date=datetime.now(), slug='job-2')
    job_posting_2.branches.set([branch_objects[0]])
    job_posting_3 = JobPosting.objects.create(id=3, company=company_object, job_type=job_type_objects_date_range[0],
                                              job_from_date=datetime.now(), slug='job-3')
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
