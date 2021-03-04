import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Benefit


class BenefitType(DjangoObjectType):
    class Meta:
        model = Benefit
        fields = ('id', 'icon',)


class BenefitQuery(ObjectType):
    benefits = graphene.List(BenefitType)

    def resolve_benefits(self, info, **kwargs):
        return Benefit.objects.all()


class BenefitInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    icon = graphene.String()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
