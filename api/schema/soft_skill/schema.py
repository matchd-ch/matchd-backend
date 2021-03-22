import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import SoftSkill


class SoftSkillType(DjangoObjectType):
    class Meta:
        model = SoftSkill
        fields = ('id', 'student', 'company',)


class SoftSkillQuery(ObjectType):
    soft_skills = graphene.List(SoftSkillType)

    def resolve_soft_skills(self, info, **kwargs):
        return SoftSkill.objects.all()
