import graphene
from django.shortcuts import get_object_or_404
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import FAQ as FAQmodel, Company


class FAQ(DjangoObjectType):
    class Meta:
        model = FAQmodel
        fields = ('id', 'category', 'title', 'question', 'answer',)
        convert_choices_to_enum = False


class FAQQuery(ObjectType):
    faqs = graphene.List(FAQ, slug=graphene.String())

    def resolve_faqs(self, info, slug):
        company = get_object_or_404(Company, slug=slug)
        faqs = company.faqs.all()
        return faqs


class FAQInput(graphene.InputObjectType):
    category = graphene.ID(required=True)
    title = graphene.String(required=False)
    question = graphene.String(required=False)
    answer = graphene.String(required=False)
