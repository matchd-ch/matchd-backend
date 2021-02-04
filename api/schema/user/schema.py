import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserNode
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

from api.schema.hobby import HobbyType
from db.models import Student as StudentModel, Hobby


class Student(DjangoObjectType):
    hobbies = graphene.List(
        HobbyType
    )

    class Meta:
        model = StudentModel
        fields = ['mobile', 'skills', 'hobbies']

    def resolve_hobbies(self, info, **kwargs):
        return Hobby.objects.filter(student=self)


class UserWithProfileNode(UserNode):
    student = graphene.Field(
        Student
    )

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
