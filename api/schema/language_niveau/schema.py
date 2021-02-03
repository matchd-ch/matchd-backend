import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import LanguageNiveau


class NiveauType(DjangoObjectType):
    class Meta:
        model = LanguageNiveau


class LanguageNiveauQuery(ObjectType):
    language_niveaus = graphene.List(NiveauType)

    def resolve_language_niveaus(self, info, **kwargs):
        return LanguageNiveau.objects.all()
