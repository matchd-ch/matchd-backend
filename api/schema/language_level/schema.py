from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import LanguageLevel as LanguageLevelModel


class LanguageLevel(DjangoObjectType):

    class Meta:
        model = LanguageLevelModel
        interfaces = (relay.Node,)
        fields = ('level', 'description',)


class LanguageLevelConnection(relay.Connection):

    class Meta:
        node = LanguageLevel


class LanguageLevelQuery(ObjectType):
    language_levels = relay.ConnectionField(LanguageLevelConnection)

    def resolve_language_levels(self, info, **kwargs):
        return LanguageLevelModel.objects.all()
