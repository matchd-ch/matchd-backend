import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Skill as SkillModel


class Skill(DjangoObjectType):
    class Meta:
        model = SkillModel
        fields = ('id', 'name',)


class SkillQuery(ObjectType):
    skills = graphene.List(Skill)

    def resolve_skills(self, info, **kwargs):
        return SkillModel.objects.all()


class SkillInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
