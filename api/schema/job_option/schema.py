import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobOption


class JobOptionDjangoType(DjangoObjectType):
    class Meta:
        model = JobOption


class JobOptionQuery(ObjectType):
    job_options = graphene.List(JobOptionDjangoType)

    def resolve_job_options(self, info, **kwargs):
        return JobOption.objects.all()


class JobOptionInputType(graphene.InputObjectType):
    id = graphene.Int(required=True)
    name = graphene.String(required=False)
    type = graphene.String(required=False)
