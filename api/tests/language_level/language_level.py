import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import LanguageLevel


class LanguageLevelGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        LanguageLevel.objects.create(name="A1")
        LanguageLevel.objects.create(name="B1")
        LanguageLevel.objects.create(name="A2")

    def test_language_query(self):
        response = self.query(
            '''
            query{
               languageLevel{
                    name
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = LanguageLevel.objects.all().count()
        self.assertEqual(
            3,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('languageLevel')[0].get('name'),
            'A1'
        )
        self.assertEqual(
            content['data'].get('languageLevel')[1].get('name'),
            'A2'
        )
        self.assertEqual(
            content['data'].get('languageLevel')[2].get('name'),
            'B1'
        )
