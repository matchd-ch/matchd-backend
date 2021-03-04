import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Branch


class BranchType(DjangoObjectType):
    class Meta:
        model = Branch
        fields = ('id', 'name',)


class BranchQuery(ObjectType):
    branches = graphene.List(BranchType)

    def resolve_branches(self, info, **kwargs):
        return Branch.objects.all()


class BranchInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
