import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobOption


class JobOptionType(DjangoObjectType):
    class Meta:
        model = JobOption
        fields = ('id', 'name', 'mode',)


class JobOptionQuery(ObjectType):
    job_options = graphene.List(JobOptionType)

    def resolve_job_options(self, info, **kwargs):
        return JobOption.objects.all()


class JobOptionInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    mode = graphene.String(required=False)
