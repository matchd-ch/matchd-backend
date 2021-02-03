import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Language


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class LanguageQuery(ObjectType):
    languages = graphene.List(LanguageType)

    def resolve_languages(self, info, **kwargs):
        return Language.objects.all()
