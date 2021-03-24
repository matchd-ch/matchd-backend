import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobOption, JobOptionMode as JobOptionModeModel

JobOptionMode = graphene.Enum.from_enum(JobOptionModeModel)


class JobOptionType(DjangoObjectType):
    mode = graphene.Field(JobOptionMode)

    class Meta:
        model = JobOption
        fields = ('id', 'name', 'mode',)
        convert_choices_to_enum = False


class JobOptionQuery(ObjectType):
    job_options = graphene.List(JobOptionType)

    def resolve_job_options(self, info, **kwargs):
        return JobOption.objects.all()


class JobOptionInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    mode = graphene.String(required=False)
