import pytest


def add_employee_mutation():
    return '''
    mutation AddEmployeeMutation($addEmployee: AddEmployeeInput!) {
        addEmployee(addEmployee: $addEmployee) {
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
                           'addEmployee': {
                               'firstName': first_name,
                               'lastName': last_name,
                               'role': role,
                               'email': email
                           }
                       },
                       **{'user': employee})

    return closure
