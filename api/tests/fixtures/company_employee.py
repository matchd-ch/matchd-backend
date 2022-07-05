import pytest

from graphql_relay import to_global_id


def add_employee_mutation():
    return '''
    mutation AddEmployeeMutation($input: AddEmployeeInput!) {
        addEmployee(input: $input) {
            success,
            errors,
            employee {
                id
                role
                firstName
                lastName
                email
            }
        }
    }
    '''


def delete_employee_mutation():
    return '''
    mutation DeleteEmployeeMutation($input: DeleteEmployeeInput!) {
        deleteEmployee(input: $input) {
            success,
            errors
        }
    }
    '''


@pytest.fixture
def add_employee(execute):

    def closure(employee, email, first_name, last_name, role):
        return execute(add_employee_mutation(),
                       variables={
                           'input': {
                               'firstName': first_name,
                               'lastName': last_name,
                               'role': role,
                               'email': email
                           }
                       },
                       **{'user': employee})

    return closure


@pytest.fixture
def delete_employee(execute):

    def closure(employee, id_to_delete):
        return execute(delete_employee_mutation(),
                       variables={'input': {
                           'id': to_global_id('User', id_to_delete)
                       }},
                       **{'user': employee})

    return closure
