import pytest

from graphql_relay import to_global_id


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


def challenge_matching():
    return '''
    mutation ChallengeMatching($input: MatchChallengeInput!){
        matchChallenge(input: $input) {
            success
            errors
            confirmed
        }
    }
    '''


@pytest.fixture
def match_job_posting(execute):

    def closure(user, job_posting_id):
        return execute(
            match_job_posting_mutation(),
            variables={"input": {
                "jobPosting": {
                    "id": to_global_id('JobPosting', job_posting_id)
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
                                   "id": to_global_id('Student', student_id)
                               },
                               "jobPosting": {
                                   "id": to_global_id('JobPosting', job_posting_id)
                               }
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def match_challenge(execute):

    def closure(user, challenge):
        return execute(
            challenge_matching(),
            variables={"input": {
                "challenge": {
                    "id": to_global_id('Challenge', challenge.id)
                }
            }},
            **{'user': user})

    return closure
