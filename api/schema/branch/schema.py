import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Branch as BranchModel


class Branch(DjangoObjectType):
    class Meta:
        model = BranchModel
        fields = ('id', 'name',)


class BranchQuery(ObjectType):
    branches = graphene.List(Branch)

    def resolve_branches(self, info, **kwargs):
        return BranchModel.objects.all()


class BranchInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
