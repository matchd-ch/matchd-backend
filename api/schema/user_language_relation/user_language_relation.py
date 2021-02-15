import graphene
from graphene_django import DjangoObjectType

from db.models import UserLanguageRelation


class UserLanguageRelationType(DjangoObjectType):
    class Meta:
        model = UserLanguageRelation


class UserLanguageRelationInputType(graphene.InputObjectType):
    id = graphene.Int()
    language = graphene.Int()
    language_level = graphene.Int()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
