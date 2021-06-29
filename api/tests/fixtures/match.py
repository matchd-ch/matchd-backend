import pytest


def match_job_posting_mutation():
    return '''
    mutation MatchMutation($match: MatchJobPostingInput!) {
      matchJobPosting(match: $match) {
        success,
        errors,
        confirmed
      }
    }
    '''


def match_student_mutation():
    return '''
    mutation MatchMutation($match: MatchStudentInput!) {
      matchStudent(match: $match) {
        success,
        errors,
        confirmed
      }
    }
    '''


def project_posting_matching():
    return '''
    mutation ProjectPostingMatching($match: MatchProjectPostingInput!){
        matchProjectPosting(match: $match) {
            success
            errors
            confirmed
        }
    }
    '''


@pytest.fixture
def match_job_posting(execute):
    def closure(user, job_posting_id):
        return execute(match_job_posting_mutation(), variables={
            "match": {
                "jobPosting": {"id": job_posting_id}
            }
        }, **{'user': user})

    return closure


@pytest.fixture
def match_student(execute):
    def closure(user, student_id, job_posting_id):
        return execute(match_student_mutation(), variables={
            "match": {
                "student": {"id": student_id},
                "jobPosting": {"id": job_posting_id}
            }
        }, **{'user': user})

    return closure


@pytest.fixture
def match_project_posting(execute):
    def closure(user, project_posting):
        return execute(project_posting_matching(), variables={
            "match": {
                "projectPosting": {
                    "id": project_posting.id
                }
            }
        }, **{'user': user})

    return closure
