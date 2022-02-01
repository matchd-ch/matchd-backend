from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import FAQCategory as FAQCategoryModel


class FAQCategory(DjangoObjectType):
    class Meta:
        model = FAQCategoryModel
        interfaces = (relay.Node,)
        fields = ('name',)


class FAQCategoryConnection(relay.Connection):
    class Meta:
        node = FAQCategory


class FAQCategoryQuery(ObjectType):
    faq_categories = relay.ConnectionField(FAQCategoryConnection)

    def resolve_faq_categories(self, info, **kwargs):
        return FAQCategoryModel.objects.all()
