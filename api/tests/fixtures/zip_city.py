import pytest

# pylint: disable=C0209


def zip_city_query():
    return '''
    query {
      zipCity {
        zip
        city
        canton
      }
    }
    '''


def zip_city_jobs_query(branch_id, job_type_id):
    return '''
    query {
      zipCityJobs(branchId: %i, jobTypeId: %i) {
        zip
      }
    }
    ''' % (branch_id, job_type_id)


@pytest.fixture
def query_zip_city(execute):

    def closure(user):
        return execute(zip_city_query(), **{'user': user})

    return closure


@pytest.fixture
def query_zip_city_jobs(execute):

    def closure(user, branch, job_type):
        return execute(zip_city_jobs_query(branch.id, job_type.id), **{'user': user})

    return closure
