import pytest


# pylint: disable=W0621


@pytest.fixture
def default_password():
    return 'asdf1234$'


def login_query(username, password):
    return '''
    mutation TokenAuth {
        tokenAuth(username: "%s", password: "%s") {
            success,
            errors,
            token
        }
    }
    ''' % (username, password)


def logout_query():
    return '''
    mutation Logout {
        logout
    }
    '''


@pytest.fixture
def login(execute, default_password):
    def closure(user, password=default_password):
        return execute(login_query(user.username, password), **{'user': user})
    return closure


@pytest.fixture
def logout(execute):
    def closure():
        return execute(logout_query())
    return closure


@pytest.fixture
def verification_url_and_token():
    def closure(email):
        activation_url = email.body.split('\n')[-2]
        return activation_url, activation_url.split('/')[-1]
    return closure


@pytest.fixture
def reset_url_and_token():
    def closure(email):
        reset_url = email.body.split('\n')[-2]
        return reset_url, reset_url.split('/')[-1]
    return closure


def send_password_reset_mail_mutation(username):
    return '''
    mutation sendPasswordResetEmail {
        sendPasswordResetEmail (
            email: "%s"
        ) 
        {
            success,
            errors
        }
    }
    ''' % username


@pytest.fixture
def send_password_reset_mail(execute):
    def closure(user):
        return execute(send_password_reset_mail_mutation(user.username), **{'user': user})
    return closure


def reset_password_mutation():
    return '''
    mutation PasswordReset($token: String!, $password1: String!, $password2: String!,  ) {
        passwordReset (
            token: $token,
            newPassword1: $password1,
            newPassword2: $password2
        ) 
        {
            success,
            errors
        }
    }
    '''


@pytest.fixture
def reset_password(execute):
    def closure(token, password1, password2):
        return execute(reset_password_mutation(),
                       variables={'token': token, 'password1': password1, 'password2': password2})
    return closure


def verify_password_reset_token_query():
    return '''
    query($token: String!) {
        verifyPasswordResetToken(token: $token)
    }
    '''


@pytest.fixture
def verify_password_reset_token(execute):
    def closure(token):
        return execute(verify_password_reset_token_query(), variables={'token': token})
    return closure


@pytest.fixture
def verify_account_query():
    return '''
    mutation VerifyAccount($token: String! ) {
      verifyAccount(token: $token) {
        success
        errors
      }
    }
    '''


@pytest.fixture
def verify_account(execute, verify_account_query):
    def closure(token):
        return execute(verify_account_query, variables={'token': token})
    return closure


@pytest.fixture
def weak_passwords():
    return (
        ('123456', 'password_too_short'),
        ('veryComplicatedPassword$ButStillWeak', 'no_digit'),
        ('$$$$$//////()()()()$1234567', 'no_letter'),
        ('veryComplicatedPasswordButStillWeak123456789', 'no_specialchars'),
    )
