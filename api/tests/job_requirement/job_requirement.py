import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import JobRequirement


class JobRequirementGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        JobRequirement.objects.create(name="Berufsmaturität (BMS)",)
        JobRequirement.objects.create(name="abgeschlossene Volksschule",)

    def test_job_requirement_query(self):
        response = self.query(
            '''
            query{
               jobRequirements{
                    id
                    name
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = JobRequirement.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('jobRequirements')[0].get('name'),
            'abgeschlossene Volksschule'
        )

        self.assertEqual(
            content['data'].get('jobRequirements')[1].get('name'),
            'Berufsmaturität (BMS)'
        )
