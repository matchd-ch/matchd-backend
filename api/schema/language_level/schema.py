import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import LanguageLevel


class LevelType(DjangoObjectType):
    class Meta:
        model = LanguageLevel


class LanguageLevelQuery(ObjectType):
    language_level = graphene.List(LevelType)

    def resolve_language_level(self, info, **kwargs):
        return LanguageLevel.objects.all()
