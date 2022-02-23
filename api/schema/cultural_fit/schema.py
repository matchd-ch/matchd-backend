import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import CulturalFit as CulturalFitModel


class CulturalFit(DjangoObjectType):

    class Meta:
        model = CulturalFitModel
        interfaces = (relay.Node, )
        fields = (
            'student',
            'company',
        )


class CulturalFitConnections(relay.Connection):

    class Meta:
        node = CulturalFit


class CulturalFitQuery(ObjectType):
    cultural_fits = relay.ConnectionField(CulturalFitConnections)

    def resolve_cultural_fits(self, info, **kwargs):
        return CulturalFitModel.objects.all()


class CulturalFitInput(graphene.InputObjectType):
    id = graphene.String(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
