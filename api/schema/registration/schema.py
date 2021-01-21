import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from graphql_auth import mutations
from graphql_auth.mutations import Register
from django.utils.translation import gettext_lazy as _
from db.forms import CompanyForm, StudentForm
from db.models import Company, Student


class CompanyInput(graphene.InputObjectType):
    role = graphene.String(description=_('Role'), required=True)
    name = graphene.String(description=_('Name'))
    uid = graphene.String(description=_('UID'), required=True)
    zip = graphene.String(description=_('ZIP'), required=True)
    city = graphene.String(description=_('City'), required=True)


# pylint: disable=R0903
# pylint: disable=R0901
class RegisterCompany(Register):

    class Arguments:
        company = CompanyInput(description=_('Company is required.'), required=True)

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
        try:
            get_user_model().validate_user_type_company(user_type)
        except ValidationError as error:
            errors.update({
                'type': [{
                    'code': error.code,
                    'message': error.message
                }]
            })

        # validate company
        company_data = data.pop('company')
        company = None

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

        company.user = user
        company.save()
        return result


class StudentInput(graphene.InputObjectType):
    mobile_number = graphene.String(description=_('Mobile'), required=True)


# pylint: disable=R0903
# pylint: disable=R0901
class RegisterStudent(Register):

    class Arguments:
        student = StudentInput(description=_('Student is required.'), required=True)

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
        try:
            get_user_model().validate_user_type_student(user_type)
        except ValidationError as error:
            errors.update({
                'type': [{
                    'code': error.code,
                    'message': error.message
                }]
            })

        # validate student
        student_data = data.pop('student')
        student = None

        student_form = StudentForm(student_data)
        student_form.full_clean()
        if student_form.is_valid():
            student = Student(**student_data)
        else:
            errors.update(student_form.errors.get_json_data())

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
        return result


class RegistrationMutation(graphene.ObjectType):
    register_company = RegisterCompany.Field()
    register_student = RegisterStudent.Field()
    verify_account = mutations.VerifyAccount.Field()
