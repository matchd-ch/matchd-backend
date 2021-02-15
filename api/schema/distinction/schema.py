import graphene
from graphene_django import DjangoObjectType

from db.models import Distinction


class DistinctionType(DjangoObjectType):
    class Meta:
        model = Distinction
        fields = ('id', 'text',)


class DistinctionInputType(graphene.InputObjectType):
    id = graphene.ID()
    text = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
