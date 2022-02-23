import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import Benefit as BenefitModel


class Benefit(DjangoObjectType):

    class Meta:
        model = BenefitModel
        interfaces = (relay.Node, )
        fields = (
            'icon',
            'name',
        )


class BenefitConnections(relay.Connection):

    class Meta:
        node = Benefit


class BenefitQuery(ObjectType):
    benefits = relay.ConnectionField(BenefitConnections)

    def resolve_benefits(self, info, **kwargs):
        return BenefitModel.objects.all()


class BenefitInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    icon = graphene.String()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
