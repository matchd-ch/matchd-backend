from datetime import datetime
import pytest

from db.models import JobPosting

# pylint: disable=W0621
# pylint: disable=R0913


def job_posting_mutation(step):
    step = str(step)
    return '''
    mutation JobPostingMutation($step%s: JobPostingInputStep%s!) {
      jobPostingStep%s(step%s: $step%s) {
        success,
        errors,
        jobPostingId
      }
    }
    ''' % (step, step, step, step, step)


@pytest.fixture
def job_posting_step_1(execute):
    def closure(user, title, description, job_type, branch, workload, job_from_date, job_to_date, url):
        return execute(job_posting_mutation(1), variables={
            'step1': {
                'title': title,
                'description': description,
                'jobType': None if job_type is None else {'id': job_type.id},
                'branch': None if branch is None else {'id': branch.id},
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
    return [
        JobPosting.objects.create(id=1, company=company_object, job_type=job_type_objects_date_range[0],
                                  job_from_date=datetime.now(), branch=branch_objects[0]),
    ]


@pytest.fixture
def job_posting_object(job_posting_objects):
    return job_posting_objects[0]
