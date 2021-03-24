import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import SoftSkill as SoftSkillModel


class SoftSkill(DjangoObjectType):
    class Meta:
        model = SoftSkillModel
        fields = ('id', 'student', 'company',)


class SoftSkillQuery(ObjectType):
    soft_skills = graphene.List(SoftSkill)

    def resolve_soft_skills(self, info, **kwargs):
        return SoftSkillModel.objects.all()
