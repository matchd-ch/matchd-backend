import pytest


def user_request_mutation():
    return '''
    mutation UserRequest($userRequest: UserRequestInput!) {
        userRequest(input: $userRequest) {
            success
            errors
        }
    }
    '''


@pytest.fixture
def user_request(execute):

    def closure(name, email, message):
        return execute(
            user_request_mutation(),
            variables={'userRequest': {
                'name': name,
                'email': email,
                'message': message
            }})

    return closure
