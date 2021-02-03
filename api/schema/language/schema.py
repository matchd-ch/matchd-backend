import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Language


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class LanguageQuery(ObjectType):
    language = graphene.Field(LanguageType, id=graphene.Int())
    languages = graphene.List(LanguageType)

    def resolve_language(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Language.objects.get(pk=id)

        return None

    def resolve_skills(self, info, **kwargs):
        return Language.objects.all()
