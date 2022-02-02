import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import JobRequirement as JobRequirementModel


class JobRequirement(DjangoObjectType):

    class Meta:
        model = JobRequirementModel
        fields = ('name', )
        interfaces = (relay.Node, )


class JobRequirementConnections(relay.Connection):

    class Meta:
        node = JobRequirement


class JobRequirementQuery(ObjectType):
    job_requirements = relay.ConnectionField(JobRequirementConnections)

    def resolve_job_requirements(self, info, **kwargs):
        return JobRequirementModel.objects.all()


class JobRequirementInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
