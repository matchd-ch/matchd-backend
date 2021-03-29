import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Language as LanguageModel


class Language(DjangoObjectType):
    class Meta:
        model = LanguageModel
        fields = ('id', 'name',)


class LanguageQuery(ObjectType):
    languages = graphene.List(Language, shortList=graphene.Boolean(required=False))

    def resolve_languages(self, info, **kwargs):
        short_list = kwargs.get('shortList', None)
        if short_list is not None:
            return LanguageModel.objects.filter(short_list=short_list)
        return LanguageModel.objects.all()
