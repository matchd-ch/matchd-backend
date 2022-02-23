import pytest


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
