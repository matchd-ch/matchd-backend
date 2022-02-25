import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import JobType as JobTypeModel, DateMode as DateModeModel

DateMode = graphene.Enum.from_enum(DateModeModel)


class JobType(DjangoObjectType):
    mode = graphene.Field(graphene.NonNull(DateMode))

    class Meta:
        model = JobTypeModel
        interfaces = (relay.Node, )
        fields = (
            'name',
            'mode',
        )
        convert_choices_to_enum = False


class JobTypeConnection(relay.Connection):

    class Meta:
        node = JobType


class JobTypeQuery(ObjectType):
    job_types = relay.ConnectionField(JobTypeConnection)

    def resolve_job_types(self, info, **kwargs):
        return JobTypeModel.objects.all()


class JobTypeInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=False)
    mode = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
