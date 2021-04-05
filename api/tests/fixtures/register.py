import pytest

# pylint: disable=W0621
# pylint: disable=R0913


@pytest.fixture
def register_student_query(default_password):
    def closure(username, first_name, last_name, mobile, password=default_password):
        return '''
        mutation RegisterStudent {
            registerStudent (
                email: "%s",
                username: "%s",
                password1: "%s",
                password2:"%s",
                firstName: "%s",
                lastName: "%s",
                type: "student",
                student: {
                    mobile: "%s"
                }
            ) 
            {
                success
                errors
            }
        }
        ''' % (username, username, password, password, first_name, last_name, mobile)
    return closure


@pytest.fixture
def register_student(execute, register_student_query, default_password):
    def closure(username, first_name, last_name, mobile, password=default_password):
        return execute(register_student_query(username, first_name, last_name, mobile, password))
    return closure


@pytest.fixture
def register_company_query(default_password):
    def closure(username, first_name, last_name, role, company_name, uid, password=default_password):
        return '''
        mutation RegisterCompany {
            registerCompany (
                email: "%s",
                username: "%s",
                password1: "%s",
                password2:"%s",
                firstName: "%s",
                lastName: "%s",
                type: "company",
                employee: {
                  role: "%s"
                }
                company: {
                  name: "%s",
                  uid: "%s",
                  zip: "0000",
                  city: "Nowhere"
                }
            ) 
            {
                success
                errors
            }
        }
        ''' % (username, username, password, password, first_name, last_name, role, company_name, uid)
    return closure


@pytest.fixture
def register_company(execute, register_company_query, default_password):
    def closure(username, first_name, last_name, role, company_name, uid, password=default_password):
        return execute(register_company_query(username, first_name, last_name, role, company_name, uid, password))
    return closure


@pytest.fixture
def register_university_query(default_password):
    def closure(username, first_name, last_name, role, company_name, password=default_password):
        return '''
        mutation RegisterCompany {
            registerCompany (
                email: "%s",
                username: "%s",
                password1: "%s",
                password2:"%s",
                firstName: "%s",
                lastName: "%s",
                type: "university",
                employee: {
                    role: "%s"
                }
                company: {
                    name: "%s",
                    zip: "0000",
                    city: "Nowhere"
                }
            ) 
            {
                success
                errors
            }
        }
        ''' % (username, username, password, password, first_name, last_name, role, company_name)
    return closure


@pytest.fixture
def register_university(execute, register_university_query, default_password):
    def closure(username, first_name, last_name, role, company_name, password=default_password):
        return execute(register_university_query(username, first_name, last_name, role, company_name, password))
    return closure
