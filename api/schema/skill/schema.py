import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import Skill as SkillModel


class Skill(DjangoObjectType):

    class Meta:
        model = SkillModel
        interfaces = (relay.Node, )
        fields = ('name', )


class SkillConnections(relay.Connection):

    class Meta:
        node = Skill


class SkillQuery(ObjectType):
    skills = relay.ConnectionField(SkillConnections)

    def resolve_skills(self, info, **kwargs):
        return SkillModel.objects.all()


class SkillInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
