import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Skill


class SkillType(DjangoObjectType):
    class Meta:
        model = Skill
        fields = ('id', 'name',)


class SkillQuery(ObjectType):
    skills = graphene.List(SkillType)

    def resolve_skills(self, info, **kwargs):
        return Skill.objects.all()


class SkillInputType(graphene.InputObjectType):
    id = graphene.Int(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
