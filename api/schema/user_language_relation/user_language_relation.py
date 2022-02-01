import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from db.models import UserLanguageRelation as UserLanguageRelationModel


class UserLanguageRelation(DjangoObjectType):

    class Meta:
        model = UserLanguageRelationModel
        interfaces = (relay.Node,)
        fields = ('language', 'language_level',)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related('language', 'language_level')


class UserLanguageRelationInput(graphene.InputObjectType):
    id = graphene.ID()
    language = graphene.ID()
    language_level = graphene.ID()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
