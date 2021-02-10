import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import UserLanguageRelation


class UserLanguageRelationType(DjangoObjectType):
    class Meta:
        model = UserLanguageRelation


class UserLanguageRelationQuery(ObjectType):
    user_language_relation = graphene.List(UserLanguageRelationType)

    def resolve_user_language_relation(self, info, **kwargs):
        return UserLanguageRelation.objects.all()


class UserLanguageRelationInputType(graphene.InputObjectType):
    id = graphene.Int()
    language = graphene.Int()
    language_level = graphene.Int()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
