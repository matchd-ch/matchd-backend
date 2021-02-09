import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Hobby


class HobbyType(DjangoObjectType):
    class Meta:
        model = Hobby


class HobbyQuery(ObjectType):
    hobby = graphene.List(HobbyType)

    def resolve_hobby(self, info, **kwargs):
        return Hobby.objects.all()


class HobbyInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String(required=False)

    @property
    def pk(self):
        return self.id
