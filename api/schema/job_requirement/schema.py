import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobRequirement as JobRequirementModel


class JobRequirement(DjangoObjectType):
    class Meta:
        model = JobRequirementModel
        fields = ('id', 'name',)


class JobRequirementQuery(ObjectType):
    job_requirements = graphene.List(JobRequirement)

    def resolve_job_requirements(self, info, **kwargs):
        return JobRequirementModel.objects.all()


class JobRequirementInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
