import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Distinction


class DistinctionType(DjangoObjectType):
    class Meta:
        model = Distinction


class DistinctionQuery(ObjectType):
    distinction = graphene.List(DistinctionType)

    def resolve_distinction(self, info, **kwargs):
        return Distinction.objects.all()


class DistinctionInputType(graphene.InputObjectType):
    id = graphene.Int()
    text = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
