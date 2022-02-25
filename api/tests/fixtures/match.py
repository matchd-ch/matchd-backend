import pytest


def match_job_posting_mutation():
    return '''
    mutation MatchMutation($input: MatchJobPostingInput!) {
      matchJobPosting(input: $input) {
        success,
        errors,
        confirmed
      }
    }
    '''


def match_student_mutation():
    return '''
    mutation MatchMutation($input: MatchStudentInput!) {
      matchStudent(input: $input) {
        success,
        errors,
        confirmed
      }
    }
    '''


def project_posting_matching():
    return '''
    mutation ProjectPostingMatching($input: MatchProjectPostingInput!){
        matchProjectPosting(input: $input) {
            success
            errors
            confirmed
        }
    }
    '''


@pytest.fixture
def match_job_posting(execute):

    def closure(user, job_posting_id):
        return execute(match_job_posting_mutation(),
                       variables={"input": {
                           "jobPosting": {
                               "id": job_posting_id
                           }
                       }},
                       **{'user': user})

    return closure


@pytest.fixture
def match_student(execute):

    def closure(user, student_id, job_posting_id):
        return execute(match_student_mutation(),
                       variables={
                           "input": {
                               "student": {
                                   "id": student_id
                               },
                               "jobPosting": {
                                   "id": job_posting_id
                               }
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def match_project_posting(execute):

    def closure(user, project_posting):
        return execute(project_posting_matching(),
                       variables={"input": {
                           "projectPosting": {
                               "id": project_posting.id
                           }
                       }},
                       **{'user': user})

    return closure
