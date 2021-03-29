import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import LanguageLevel as LanguageLevelModel


class LanguageLevel(DjangoObjectType):
    class Meta:
        model = LanguageLevelModel
        fields = ('id', 'level', 'description',)


class LanguageLevelQuery(ObjectType):
    language_levels = graphene.List(LanguageLevel)

    def resolve_language_levels(self, info, **kwargs):
        return LanguageLevelModel.objects.all()
