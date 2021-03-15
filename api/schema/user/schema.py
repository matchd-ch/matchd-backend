import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserNode
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

from db.models import Student as StudentModel, Employee as EmployeeModel, User


class Student(DjangoObjectType):

    class Meta:
        model = StudentModel
        fields = ('mobile', 'street', 'zip', 'city', 'date_of_birth', 'nickname', 'school_name', 'field_of_study',
                  'graduation', 'skills', 'hobbies', 'languages', 'distinction', 'online_projects',)


class Employee(DjangoObjectType):
    user = graphene.Field(UserNode)

    class Meta:
        model = EmployeeModel
        fields = ('id', 'role',)

    def resolve_users(self, info):
        user = self.user
        return User.objects.get(username=user)


class UserWithProfileNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (graphene.relay.Node,)
        skip_registry = True


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserWithProfileNode)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
