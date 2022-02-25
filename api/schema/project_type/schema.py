import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import ProjectType as ProjectTypeModel


class ProjectType(DjangoObjectType):

    class Meta:
        model = ProjectTypeModel
        interfaces = (relay.Node, )
        fields = ('name', )
        convert_choices_to_enum = False


class ProjectTypeConnection(relay.Connection):

    class Meta:
        node = ProjectType


class ProjectTypeQuery(ObjectType):
    project_types = relay.ConnectionField(ProjectTypeConnection)

    def resolve_project_types(self, info, **kwargs):
        return ProjectTypeModel.objects.all()


class ProjectTypeInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=False)
