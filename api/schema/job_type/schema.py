import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import JobType as JobTypeModel, DateMode as DateModeModel

DateMode = graphene.Enum.from_enum(DateModeModel)


class JobType(DjangoObjectType):
    mode = graphene.Field(graphene.NonNull(DateMode))

    class Meta:
        model = JobTypeModel
        fields = ('id', 'name', 'mode',)
        convert_choices_to_enum = False


class JobTypeQuery(ObjectType):
    job_types = graphene.List(JobType)

    def resolve_job_types(self, info, **kwargs):
        return JobTypeModel.objects.all()


class JobTypeInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    mode = graphene.String(required=False)
