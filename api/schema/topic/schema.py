import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Topic as TopicModel


class Topic(DjangoObjectType):

    class Meta:
        model = TopicModel
        fields = ('id', 'name', )
        convert_choices_to_enum = False


class TopicQuery(ObjectType):
    topics = graphene.List(Topic)

    def resolve_topics(self, info, **kwargs):
        return TopicModel.objects.all()


class TopicInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
