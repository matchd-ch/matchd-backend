import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import Language


class LanguageGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        Language.objects.create(name="Zulu")
        Language.objects.create(name="Deutsch")
        Language.objects.create(name="Englisch")

    def test_language_query(self):
        response = self.query(
            '''
            query{
               languages{
                    name
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = Language.objects.all().count()
        self.assertEqual(
            3,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('languages')[0].get('name'),
            'Deutsch'
        )
        self.assertEqual(
            content['data'].get('languages')[1].get('name'),
            'Englisch'
        )
        self.assertEqual(
            content['data'].get('languages')[2].get('name'),
            'Zulu'
        )
