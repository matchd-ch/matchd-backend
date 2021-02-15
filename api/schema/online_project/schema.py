import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import OnlineProject


class OnlineProjectType(DjangoObjectType):
    class Meta:
        model = OnlineProject
        fields = ('id', 'url',)


class OnlineProjectQuery(ObjectType):
    online_project = graphene.List(OnlineProjectType)

    def resolve_online_project(self, info, **kwargs):
        return OnlineProject.objects.all()


class OnlineProjectInputType(graphene.InputObjectType):
    id = graphene.Int()
    url = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
