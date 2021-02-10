import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import JobOption, JobOptionMode


class JobOptionGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        JobOption.objects.create(name="Praktikum", mode=JobOptionMode.DATE_FROM)
        JobOption.objects.create(name="Lehrstelle", mode=JobOptionMode.DATE_RANGE)

    def test_job_option_query(self):
        response = self.query(
            '''
            query{
               jobOptions{
                    name
                    mode
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
