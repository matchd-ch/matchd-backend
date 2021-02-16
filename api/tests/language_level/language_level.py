import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import LanguageLevel


class LanguageLevelGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        LanguageLevel.objects.create(level="A1")
        LanguageLevel.objects.create(level="B1")
        LanguageLevel.objects.create(level="A2")

    def test_language_query(self):
        response = self.query(
            '''
            query{
               languageLevels{
                    level
                    description
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
            content['data'].get('languageLevels')[0].get('level'),
            'A1'
        )
        self.assertEqual(
            content['data'].get('languageLevels')[1].get('level'),
            'A2'
        )
        self.assertEqual(
            content['data'].get('languageLevels')[2].get('level'),
            'B1'
        )
