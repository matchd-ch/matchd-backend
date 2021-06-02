import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import ProjectType as ProjectTypeModel


class ProjectType(DjangoObjectType):

    class Meta:
        model = ProjectTypeModel
        fields = ('id', 'name', )
        convert_choices_to_enum = False


class ProjectTypeQuery(ObjectType):
    project_types = graphene.List(ProjectType)

    def resolve_project_types(self, info, **kwargs):
        return ProjectTypeModel.objects.all()


class ProjectTypeInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
