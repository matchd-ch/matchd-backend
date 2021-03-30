import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Expectation as ExpectationModel


class Expectation(DjangoObjectType):
    class Meta:
        model = ExpectationModel
        fields = ('id', 'name',)


class ExpectationQuery(ObjectType):
    expectations = graphene.List(Expectation)

    def resolve_expectations(self, info, **kwargs):
        return ExpectationModel.objects.all()


class ExpectationInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
