import graphene
from graphene_django import DjangoObjectType

from db.models import Hobby as HobbyModel


class Hobby(DjangoObjectType):
    class Meta:
        model = HobbyModel
        fields = ('id', 'name',)


class HobbyInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
