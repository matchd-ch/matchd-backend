import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import CulturalFit as CulturalFitModel


class CulturalFit(DjangoObjectType):
    class Meta:
        model = CulturalFitModel
        fields = ('id', 'student', 'company',)


class CulturalFitQuery(ObjectType):
    cultural_fits = graphene.List(CulturalFit)

    def resolve_cultural_fits(self, info, **kwargs):
        return CulturalFitModel.objects.all()


class CulturalFitInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
