import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import ChallengeType as ChallengeTypeModel


class ChallengeType(DjangoObjectType):

    class Meta:
        model = ChallengeTypeModel
        interfaces = (relay.Node, )
        fields = ('name', )
        convert_choices_to_enum = False


class ChallengeTypeConnection(relay.Connection):

    class Meta:
        node = ChallengeType


class ChallengeTypeQuery(ObjectType):
    challenge_types = relay.ConnectionField(ChallengeTypeConnection)

    def resolve_challenge_types(self, info, **kwargs):
        return ChallengeTypeModel.objects.all()


class ChallengeTypeInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=False)
