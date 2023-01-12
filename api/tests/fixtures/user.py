import pytest

from django.contrib.auth import get_user_model


def delete_user_mutation():
    return '''
    mutation DeleteUser($input: DeleteUserMutationInput!) {
      deleteUser(input: $input) {
        success,
        errors
      }
    }
    '''


@pytest.fixture
def delete_user(execute):

    def closure(user):
        return execute(delete_user_mutation(), variables={"input": {}}, **{'user': user})

    return closure


def update_user_mutation():
    return '''
    mutation UpdateUser($input: UpdateUserMutationInput!) {
      updateUser(input: $input) {
        success,
        errors,
        user {
            id
            email
        }
      }
    }
    '''


def resend_activation_email_mutation():
    return '''
    mutation ResendActivationEmail($email: String!) {
      resendActivationEmail(email: $email) {
        success,
        errors
      }
    }
    '''


def change_user_password_mutation():
    return '''
    mutation PasswordChange($oldPassword: String!, $newPassword1: String!, $newPassword2: String!) {
      passwordChange(oldPassword: $oldPassword, newPassword1: $newPassword1, newPassword2: $newPassword2) {
        success,
        errors
      }
    }
    '''


@pytest.fixture
def get_user():

    def closure(username, password, verified, user_type, company=None):
        # pylint: disable=W0612
        user, created = get_user_model().objects.get_or_create(username=username,
                                                               email=username,
                                                               type=user_type,
                                                               company=company)
        user.set_password(password)
        user.save()
        user.status.verified = verified
        user.status.save()
        return user

    return closure


@pytest.fixture
def update_user(execute):

    def closure(user, user_data):
        return execute(update_user_mutation(), variables={"input": {**user_data}}, **{'user': user})

    return closure


@pytest.fixture
def resend_activation_email(execute):

    def closure(email):
        return execute(resend_activation_email_mutation(), variables={"email": email}, **{})

    return closure


@pytest.fixture
def change_user_password(execute):

    def closure(user, old_password, new_password):
        return execute(change_user_password_mutation(),
                       variables={
                           "oldPassword": old_password,
                           "newPassword1": new_password,
                           "newPassword2": new_password
                       },
                       **{'user': user})

    return closure
