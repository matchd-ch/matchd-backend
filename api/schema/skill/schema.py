import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Skill


class SkillType(DjangoObjectType):
    class Meta:
        model = Skill


class SkillQuery(ObjectType):
    skill = graphene.Field(SkillType, id=graphene.Int())
    skills = graphene.List(SkillType)

    def resolve_skill(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Skill.objects.get(pk=id)

        return None

    def resolve_skills(self, info, **kwargs):
        return Skill.objects.all()
