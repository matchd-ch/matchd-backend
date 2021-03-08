import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Expectation


class ExpectationType(DjangoObjectType):
    class Meta:
        model = Expectation
        fields = ('id', 'name',)


class ExpectationQuery(ObjectType):
    expectations = graphene.List(ExpectationType)

    def resolve_expectations(self, info, **kwargs):
        return Expectation.objects.all()


class ExpectationInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
