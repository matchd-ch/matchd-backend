import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobOption, Branch


class BranchType(DjangoObjectType):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'mode',)


class BranchQuery(ObjectType):
    branch = graphene.List(BranchType)

    def resolve_branch(self, info, **kwargs):
        return Branch.objects.all()


class BranchInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

