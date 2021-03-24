import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

from db.models import Student as StudentModel, Employee as EmployeeModel, ProfileState as ProfileStateModel, \
    ProfileType as ProfileTypeModel


ProfileState = graphene.Enum.from_enum(ProfileStateModel)
ProfileType = graphene.Enum.from_enum(ProfileTypeModel)


class Student(DjangoObjectType):
    state = graphene.Field(ProfileState)

    class Meta:
        model = StudentModel
        fields = ('mobile', 'street', 'zip', 'city', 'date_of_birth', 'nickname', 'school_name', 'field_of_study',
                  'graduation', 'skills', 'hobbies', 'languages', 'distinction', 'online_projects', 'state',
                  'profile_step')
        convert_choices_to_enum = False


class UserWithProfileNode(DjangoObjectType):
    type = graphene.Field(ProfileType)

    class Meta:
        model = get_user_model()
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (graphene.relay.Node,)
        skip_registry = True
        convert_choices_to_enum = False


class Employee(DjangoObjectType):
    user = graphene.Field(UserWithProfileNode)

    class Meta:
        model = EmployeeModel
        fields = ['id', 'role', 'user']

    def resolve_user(self, info):
        return self.user


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserWithProfileNode)

    @login_required
    def resolve_me(self, info):
        user = info.context.user

        if user.is_authenticated:
            user = get_user_model().objects.prefetch_related('student', 'company__users',
                                                             'company__benefits', 'company__job_positions').\
                select_related('company', 'company__branch').get(pk=user.id)
            return user
        return None
