import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Skill


class SkillType(DjangoObjectType):
    class Meta:
        model = Skill


class SkillQuery(ObjectType):
    skills = graphene.List(SkillType)

    def resolve_skills(self, info, **kwargs):
        return Skill.objects.all()
