import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import LanguageNiveau


class LanguageNiveauGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        LanguageNiveau.objects.create(name="A1")
        LanguageNiveau.objects.create(name="B1")
        LanguageNiveau.objects.create(name="A2")

    def test_language_query(self):
        response = self.query(
            '''
            query{
               languageNiveaus{
                    name
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = LanguageNiveau.objects.all().count()
        self.assertEqual(
            3,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('languageNiveaus')[0].get('name'),
            'A1'
        )
        self.assertEqual(
            content['data'].get('languageNiveaus')[1].get('name'),
            'A2'
        )
        self.assertEqual(
            content['data'].get('languageNiveaus')[2].get('name'),
            'B1'
        )
