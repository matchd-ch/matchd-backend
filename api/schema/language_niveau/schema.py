import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import LanguageNiveau


class NiveauType(DjangoObjectType):
    class Meta:
        model = LanguageNiveau


class LanguageNiveauQuery(ObjectType):
    languageNiveau = graphene.Field(NiveauType, id=graphene.Int())
    languageNiveaus = graphene.List(NiveauType)

    def resolve_languageNiveau(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return LanguageNiveau.objects.get(pk=id)

        return None

    def resolve_languageNiveaus(self, info, **kwargs):
        return LanguageNiveau.objects.all()
