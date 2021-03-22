import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import FAQCategory


class FAQCategoryType(DjangoObjectType):
    class Meta:
        model = FAQCategory
        fields = ('id', 'name',)


class FAQCategoryQuery(ObjectType):
    faq_categories = graphene.List(FAQCategoryType)

    def resolve_categories(self, info, **kwargs):
        return FAQCategory.objects.all()
