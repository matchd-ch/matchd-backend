import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import CulturalFit


class CulturalFitGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        CulturalFit.objects.create(id=1, student="I like working", company='You like working')
        CulturalFit.objects.create(id=2, student="I like things", company='You like things')

    def test_cultural_fit_query(self):
        response = self.query(
            '''
            query{
               culturalFits{
                    id
                    student
                    company
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = CulturalFit.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        self.assertEqual(
            content['data'].get('culturalFits')[0].get('company'),
            'You like working'
        )
        self.assertEqual(
            content['data'].get('culturalFits')[0].get('student'),
            'I like working'
        )
        self.assertEqual(
            content['data'].get('culturalFits')[1].get('company'),
            'You like things'
        )
        self.assertEqual(
            content['data'].get('culturalFits')[1].get('student'),
            'I like things'
        )
