import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import Category


class CategoryGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        Category.objects.create(id=1, name="Zweite Category")
        Category.objects.create(id=2, name="Erste Category")


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
        num_entries = Category.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('categories')[0].get('name'),
            'Erste Category'
        )

        self.assertEqual(
            content['data'].get('categories')[1].get('name'),
            'Zweite Category'
        )
