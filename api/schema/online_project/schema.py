import graphene
from graphene_django import DjangoObjectType

from db.models import OnlineProject as OnlineProjectModel


class OnlineProject(DjangoObjectType):
    class Meta:
        model = OnlineProjectModel
        fields = ('id', 'url',)


class OnlineProjectInput(graphene.InputObjectType):
    id = graphene.ID()
    url = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
