import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import Branch


class BranchGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        Branch.objects.create(name="Systemtechnik",)
        Branch.objects.create(name="Applikationsentwicklung",)

    def test_branches_query(self):
        response = self.query(
            '''
            query{
               branches{
                    id
                    name
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = Branch.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('branches')[0].get('name'),
            'Applikationsentwicklung'
        )

        self.assertEqual(
            content['data'].get('branches')[1].get('name'),
            'Systemtechnik'
        )
