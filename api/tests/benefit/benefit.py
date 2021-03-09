import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import Benefit


class BenefitGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        Benefit.objects.create(name="Massage", icon='spa')
        Benefit.objects.create(name="Laptop", icon='laptop')

    def test_benefit_query(self):
        response = self.query(
            '''
            query{
               benefits{
                    id
                    name
                    icon
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = Benefit.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('benefits')[0].get('name'),
            'Laptop'
        )

        self.assertEqual(
            content['data'].get('benefits')[1].get('name'),
            'Massage'
        )
