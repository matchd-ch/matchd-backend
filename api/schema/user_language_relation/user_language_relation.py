import graphene
from graphene_django import DjangoObjectType

from db.models import UserLanguageRelation


class UserLanguageRelationType(DjangoObjectType):
    class Meta:
        model = UserLanguageRelation


class UserLanguageRelationInputType(graphene.InputObjectType):
    id = graphene.ID()
    language = graphene.ID()
    language_level = graphene.ID()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
