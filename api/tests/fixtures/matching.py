import pytest

# pylint: disable=C0209


def job_posting_matching_query(tech_boost, soft_boost):
    return '''
    query JobPostingMatching($jobPostingMatching: JobPostingMatchingInput){
      matches (jobPostingMatching: $jobPostingMatching, techBoost: %i, softBoost: %i) {
        id
        name
        avatar
        type
        slug
        score
        rawScore
        title
        matchStatus {
          confirmed
          initiator
        }
      }
    }
    ''' % (tech_boost, soft_boost)


def student_matching_query(tech_boost, soft_boost):
    return '''
    query StudentMatching($studentMatching: StudentMatchingInput){
      matches (studentMatching: $studentMatching, techBoost: %i, softBoost: %i) {
        id
        name
        avatar
        type
        slug
        score
        rawScore
        title
        matchStatus {
          confirmed
          initiator
        }
      }
    }
    ''' % (tech_boost, soft_boost)


def company_matching_query(tech_boost, soft_boost):
    return '''
    query {
      matches (techBoost: %i, softBoost: %i) {
        id
        name
        avatar
        type
        slug
        score
        rawScore
        title
        matchStatus {
          confirmed
          initiator
        }
      }
    }
    ''' % (tech_boost, soft_boost)


@pytest.fixture
def job_posting_matching(execute):

    def closure(user, branch, job_type, tech_boost=1, soft_boost=1):
        return execute(job_posting_matching_query(tech_boost, soft_boost),
                       variables={
                           "jobPostingMatching": {
                               "branch": {
                                   "id": branch.id
                               },
                               "jobType": {
                                   "id": job_type.id
                               }
                           }
                       },
                       **{'user': user})

    return closure


@pytest.fixture
def student_matching(execute):

    def closure(user, job_posting, tech_boost=1, soft_boost=1):
        return execute(student_matching_query(tech_boost, soft_boost),
                       variables={"studentMatching": {
                           "jobPosting": {
                               "id": job_posting.id
                           }
                       }},
                       **{'user': user})

    return closure


@pytest.fixture
def company_matching(execute):

    def closure(user, tech_boost=1, soft_boost=1):
        return execute(company_matching_query(tech_boost, soft_boost), **{'user': user})

    return closure
