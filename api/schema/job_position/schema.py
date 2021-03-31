import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobPosition as JobPositionModel


class JobPosition(DjangoObjectType):
    class Meta:
        model = JobPositionModel
        fields = ('id', 'name',)


class JobPositionQuery(ObjectType):
    job_positions = graphene.List(JobPosition)

    def resolve_job_positions(self, info, **kwargs):
        return JobPositionModel.objects.all()


class JobPositionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
