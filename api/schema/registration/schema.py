import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from graphql_auth import mutations
from graphql_auth.mutations import Register
from django.utils.translation import gettext_lazy as _

from api.schema.error import ErrorType
from db.models import Company, Student, UserType


class CompanyInput(graphene.InputObjectType):
    role = graphene.String(description=_('Role'))
    name = graphene.String(description=_('Name'))
    uid = graphene.String(description=_('UID'))
    zip = graphene.String(description=_('ZIP'))
    city = graphene.String(description=_('City'))


# pylint: disable=R0903
# pylint: disable=R0901
class RegisterCompany(Register):

    class Arguments:
        company = CompanyInput(description=_('Company is required.'), required=True)

    class Meta:
        description = _('Creates a new user with company')

    @classmethod
    def mutate(cls, root, info, **data):
        try:
            company = Company(**data.get('company'))
            company.full_clean(exclude=['user'])
        except ValidationError as error:
            return RegisterCompany(success=False, errors=ErrorType.serialize(error.message_dict))

        data['type'] = UserType.COMPANY

        result = cls.resolve_mutation(root, info, **data)
        if result.errors:
            return RegisterCompany(success=False, errors=ErrorType.serialize(result.errors))

        try:
            user = get_user_model().objects.get(email=data.get('email'))
        except get_user_model().DoesNotExist:
            return RegisterCompany(success=False, errors={'non_field_errors': 'User not found.'})

        company.user = user
        company.save()
        return result


class StudentInput(graphene.InputObjectType):
    mobile_number = graphene.String(description=_('MobileNumber'))


# pylint: disable=R0903
# pylint: disable=R0901
class RegisterStudent(Register):

    class Arguments:
        student = StudentInput(description=_('Student is required.'), required=True)

    class Meta:
        description = _('Creates a new user as student')

    @classmethod
    def mutate(cls, root, info, **data):
        try:
            student = Student(**data.get('student'))
            student.full_clean(exclude=['user'])
        except ValidationError as error:
            return RegisterStudent(success=False, errors=ErrorType.serialize(error.message_dict))

        data['type'] = UserType.STUDENT

        result = cls.resolve_mutation(root, info, **data)
        if result.errors:
            return RegisterStudent(success=False, errors=ErrorType.serialize(result.errors))

        try:
            user = get_user_model().objects.get(email=data.get('email'))
        except get_user_model().DoesNotExist:
            return RegisterCompany(success=False, errors={'non_field_errors': 'User not found.'})
        student.user = user
        student.save()
        return result


class RegistrationMutation(graphene.ObjectType):
    register_company = RegisterCompany.Field()
    register_student = RegisterStudent.Field()
    verify_account = mutations.VerifyAccount.Field()
