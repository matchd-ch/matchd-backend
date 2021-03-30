import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Benefit as BenefitModel


class Benefit(DjangoObjectType):
    class Meta:
        model = BenefitModel
        fields = ('id', 'icon', 'name',)


class BenefitQuery(ObjectType):
    benefits = graphene.List(Benefit)

    def resolve_benefits(self, info, **kwargs):
        return BenefitModel.objects.all()


class BenefitInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    icon = graphene.String()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
