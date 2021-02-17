import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobPosition


class JobPositionType(DjangoObjectType):
    class Meta:
        model = JobPosition
        fields = ('id', 'name',)


class JobPositionQuery(ObjectType):
    job_positions = graphene.List(JobPositionType)

    def resolve_job_positions(self, info, **kwargs):
        return JobPosition.objects.all()


class JobPositionInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
