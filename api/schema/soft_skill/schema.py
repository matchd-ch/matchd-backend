import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import SoftSkill as SoftSkillModel


class SoftSkill(DjangoObjectType):

    class Meta:
        model = SoftSkillModel
        interfaces = (relay.Node, )
        fields = (
            'student',
            'company',
        )


class SoftSkillConnections(relay.Connection):

    class Meta:
        node = SoftSkill


class SoftSkillQuery(ObjectType):
    soft_skills = relay.ConnectionField(SoftSkillConnections)

    def resolve_soft_skills(self, info, **kwargs):
        return SoftSkillModel.objects.all()


class SoftSkillInput(graphene.InputObjectType):
    id = graphene.String(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
