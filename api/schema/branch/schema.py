import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import Branch as BranchModel


class Branch(DjangoObjectType):

    class Meta:
        model = BranchModel
        interfaces = (relay.Node, )
        fields = ('name', )


class BranchConnections(relay.Connection):

    class Meta:
        node = Branch


class BranchQuery(ObjectType):
    branches = relay.ConnectionField(BranchConnections)

    def resolve_branches(self, info, **kwargs):
        return BranchModel.objects.all()


class BranchInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
