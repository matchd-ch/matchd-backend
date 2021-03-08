import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Language


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language
        fields = ('id', 'name',)


class LanguageQuery(ObjectType):
    languages = graphene.List(LanguageType, shortList=graphene.Boolean(required=False))

    def resolve_languages(self, info, **kwargs):
        short_list = kwargs.get('shortList', None)
        if short_list is not None:
            return Language.objects.filter(short_list=short_list)
        return Language.objects.all()
