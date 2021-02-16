import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import LanguageLevel


class LevelType(DjangoObjectType):
    class Meta:
        model = LanguageLevel
        fields = ('id', 'level', 'description',)


class LanguageLevelQuery(ObjectType):
    language_levels = graphene.List(LevelType)

    def resolve_language_levels(self, info, **kwargs):
        return LanguageLevel.objects.all()
