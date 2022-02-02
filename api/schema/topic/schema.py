import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import Topic as TopicModel


class Topic(DjangoObjectType):

    class Meta:
        model = TopicModel
        interfaces = (relay.Node, )
        fields = ('name', )
        convert_choices_to_enum = False


class TopicConnection(relay.Connection):

    class Meta:
        node = Topic


class TopicQuery(ObjectType):
    topics = relay.ConnectionField(TopicConnection)

    def resolve_topics(self, info, **kwargs):
        return TopicModel.objects.all()


class TopicInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
