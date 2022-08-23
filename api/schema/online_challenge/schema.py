import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from db.models import OnlineChallenge as OnlineChallengeModel


class OnlineChallenge(DjangoObjectType):

    class Meta:
        model = OnlineChallengeModel
        interfaces = (relay.Node, )
        fields = ('url', )


class OnlineChallengeInput(graphene.InputObjectType):
    id = graphene.String()
    url = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
