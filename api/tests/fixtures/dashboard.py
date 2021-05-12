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
      }
    }
    '''


@pytest.fixture
def query_dashboard(execute):
    def closure(user):
        return execute(dashboard_query(), **{'user': user})
    return closure
