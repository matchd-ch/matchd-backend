import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import FAQCategory as FAQCategoryModel


class FAQCategory(DjangoObjectType):
    class Meta:
        model = FAQCategoryModel
        fields = ('id', 'name', 'faqs',)


class FAQCategoryQuery(ObjectType):
    faq_categories = graphene.List(FAQCategory)

    def resolve_faq_categories(self, info, **kwargs):
        return FAQCategoryModel.objects.all()


class FAQCategoryInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
