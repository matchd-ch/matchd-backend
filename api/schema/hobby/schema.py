import graphene
from graphene_django import DjangoObjectType

from db.models import Hobby


class HobbyType(DjangoObjectType):
    class Meta:
        model = Hobby
        fields = ('id', 'name',)


class HobbyInputType(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
