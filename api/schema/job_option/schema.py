import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobOption as JobOptionModel, JobOptionMode as JobOptionModeModel

JobOptionMode = graphene.Enum.from_enum(JobOptionModeModel)


class JobOption(DjangoObjectType):
    mode = graphene.Field(JobOptionMode)

    class Meta:
        model = JobOptionModel
        fields = ('id', 'name', 'mode',)
        convert_choices_to_enum = False


class JobOptionQuery(ObjectType):
    job_options = graphene.List(JobOption)

    def resolve_job_options(self, info, **kwargs):
        return JobOptionModel.objects.all()


class JobOptionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    mode = graphene.String(required=False)
