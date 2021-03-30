import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import JobType, DateMode


class JobTypeGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        JobType.objects.create(name="Praktikum", mode=DateMode.DATE_FROM)
        JobType.objects.create(name="Lehrstelle", mode=DateMode.DATE_RANGE)

    def test_job_type_query(self):
        response = self.query(
            '''
            query{
               jobTypes{
                    id
                    name
                    mode
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = JobType.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('jobTypes')[0].get('name'),
            'Lehrstelle'
        )
        self.assertEqual(
            content['data'].get('jobTypes')[1].get('name'),
            'Praktikum'
        )
