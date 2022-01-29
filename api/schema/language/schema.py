import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import Language as LanguageModel


class Language(DjangoObjectType):

    class Meta:
        model = LanguageModel
        interfaces = (relay.Node,)
        fields = ('name',)


class LanguageConnection(relay.Connection):

    class Meta:
        node = Language


class LanguageQuery(ObjectType):
    languages = relay.ConnectionField(LanguageConnection, shortList=graphene.Boolean(required=False))

    def resolve_languages(self, info, **kwargs):
        short_list = kwargs.get('shortList', None)
        if short_list is not None:
            return LanguageModel.objects.filter(short_list=short_list)
        return LanguageModel.objects.all()
