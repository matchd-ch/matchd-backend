import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import JobOption, JobOptionType


class JobOptionGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        JobOption.objects.create(name="Praktikum", type=JobOptionType.DATE_FROM)
        JobOption.objects.create(name="Lehrstelle", type=JobOptionType.DATE_RANGE)

    def test_job_option_query(self):
        response = self.query(
            '''
            query{
               jobOptions{
                    name
                    type
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = JobOption.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('jobOptions')[0].get('name'),
            'Lehrstelle'
        )
        self.assertEqual(
            content['data'].get('jobOptions')[1].get('name'),
            'Praktikum'
        )
