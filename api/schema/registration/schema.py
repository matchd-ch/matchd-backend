from graphene import ObjectType
from graphql_auth.mutations import Register, VerifyAccount, ResendActivationEmail

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from api.helper import notify_managers_new_user_registration
from api.schema.company import RegisterCompanyInput
from api.schema.employee import EmployeeInput
from api.schema.student import RegisterStudentInput

from db.helper import generic_error_dict, get_company_slug
from db.forms import CompanyForm, StudentForm, EmployeeForm, UniversityForm
from db.models import Company, Student, Employee, ProfileType


class RegisterCompany(Register):

    class Arguments:
        company = RegisterCompanyInput(description=_('Company is required.'), required=True)
        employee = EmployeeInput(description=_('Employee is required.'), required=True)

    class Meta:
        description = _('Creates a new user with company')

    @classmethod
    def mutate(cls, root, info, **data):
        errors = {}

        # Validate all models before writing to the database
        # we need to provide a list with errors to the frontend across both models

        # validate user type
        # allowed types: company, university
        user_type = data.get('type')

        if user_type not in ProfileType.valid_company_types():
            errors.update(
                generic_error_dict('type', _('You are not part of a company'), 'invalid_type'))

        # validate employee
        employee_data = data.pop('employee')
        employee = None

        employee_form = EmployeeForm(employee_data)
        employee_form.full_clean()
        if employee_form.is_valid():
            employee = Employee(**employee_data)
        else:
            errors.update(employee_form.errors.get_json_data())

        # validate company
        company_data = data.pop('company')
        company_data['slug'] = get_company_slug(company_data.get('name'))
        company_data['type'] = user_type
        company = None

        if user_type == ProfileType.UNIVERSITY:
            company_form = UniversityForm(company_data)
        else:
            company_form = CompanyForm(company_data)

        company_form.full_clean()
        if company_form.is_valid():
            company = Company(**company_data)
        else:
            errors.update(company_form.errors.get_json_data())

        # validate user
        user_data = data
        register_form = cls.form(user_data)
        register_form.full_clean()
        if not register_form.is_valid():
            errors.update(register_form.errors.get_json_data())

        if errors:
            return RegisterCompany(success=False, errors=errors)

        result = cls.resolve_mutation(root, info, **data)
        user = get_user_model().objects.get(email=user_data.get('email'))

        company.save()

        user.company = company
        user.save()

        employee.user = user
        employee.save()

        notify_managers_new_user_registration(user)

        return result


class RegisterStudent(Register):

    class Arguments:
        student = RegisterStudentInput(description=_('Student is optional.'))

    class Meta:
        description = _('Creates a new user as student')

    @classmethod
    def mutate(cls, root, info, **data):
        errors = {}

        # Validate all models before writing to the database
        # we need to provide a list with errors to the frontend across both models

        # validate user type
        # allowed types: student, college-student, junior
        user_type = data.get('type')

        if user_type not in ProfileType.valid_student_types():
            errors.update(generic_error_dict('type', _('You are not a student'), 'invalid_type'))

        # validate student
        student_data = data.pop('student', None)
        student = None

        if student_data is not None:
            student_form = StudentForm(student_data)
            student_form.full_clean()
            if student_form.is_valid():
                student = Student(**student_data)
            else:
                errors.update(student_form.errors.get_json_data())
        else:
            student = Student()

        # validate user
        user_data = data
        register_form = cls.form(user_data)
        register_form.full_clean()
        if not register_form.is_valid():
            errors.update(register_form.errors.get_json_data())

        if errors:
            return RegisterStudent(success=False, errors=errors)

        result = cls.resolve_mutation(root, info, **data)
        user = get_user_model().objects.get(email=data.get('email'))

        student.user = user
        student.save()

        notify_managers_new_user_registration(user)

        return result


class RegistrationMutation(ObjectType):
    register_company = RegisterCompany.Field()
    register_student = RegisterStudent.Field()
    verify_account = VerifyAccount.Field()
    resend_activation_email = ResendActivationEmail.Field()
