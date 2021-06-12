import pytest


def dashboard_query():
    return '''
    query {
      dashboard {
        jobPostings {
          id
          title
          datePublished
          dateCreated
        }
        projectPostings {
          id
          title
          datePublished
          dateCreated
        }
        latestJobPostings {
          id
          title
          datePublished
          dateCreated
        }
        latestProjectPostings {
          id
          title
          datePublished
          dateCreated
        }
        requestedMatches {
          jobPosting {
            id
            title
          }
          student {
            nickname
          }
        }
        unconfirmedMatches {
          jobPosting {
            id
            title
          }
          student {
            nickname
          }
        }
        confirmedMatches {
          jobPosting {
            id
            title
          }
          student {
            nickname
          }
        }
        projectMatches {
          projectPosting {
            id
            title
          }
          student {
            nickname
          }
          company {
            id
          }
        }
      }
    }
    '''


@pytest.fixture
def query_dashboard(execute):
    def closure(user):
        return execute(dashboard_query(), **{'user': user})
    return closure
