import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from db.models import Hobby as HobbyModel


class Hobby(DjangoObjectType):

    class Meta:
        model = HobbyModel
        interfaces = (relay.Node, )
        fields = ('name', )


class HobbyInput(graphene.InputObjectType):
    id = graphene.String()
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
