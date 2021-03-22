import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import FAQCategory


class FAQCategoryGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        FAQCategory.objects.create(id=1, name="Zweite Category")
        FAQCategory.objects.create(id=2, name="Erste Category")


    def test_category_query(self):
        response = self.query(
            '''
            query{
                categories{
                    id
                    name
                }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = FAQCategory.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('faq_categories')[0].get('name'),
            'Erste Category'
        )

        self.assertEqual(
            content['data'].get('faq_categories')[1].get('name'),
            'Zweite Category'
        )
