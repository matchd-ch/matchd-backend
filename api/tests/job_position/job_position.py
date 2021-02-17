import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import JobPosition


class JobPositionGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        JobPosition.objects.create(name="Systemtechniker*in")
        JobPosition.objects.create(name="Applikationsentwickler*in")

    def test_job_position_query(self):
        response = self.query(
            '''
            query{
               jobPositions{
                    id
                    name
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = JobPosition.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('jobPositions')[0].get('name'),
            'Applikationsentwickler*in'
        )
        self.assertEqual(
            content['data'].get('jobPositions')[1].get('name'),
            'Systemtechniker*in'
        )
