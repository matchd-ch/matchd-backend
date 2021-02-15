import graphene
from graphene_django import DjangoObjectType

from db.models import OnlineProject


class OnlineProjectType(DjangoObjectType):
    class Meta:
        model = OnlineProject
        fields = ('id', 'url',)


class OnlineProjectInputType(graphene.InputObjectType):
    id = graphene.ID()
    url = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
