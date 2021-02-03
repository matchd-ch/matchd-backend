import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import Skill


class SkillGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        Skill.objects.create(name="php")
        Skill.objects.create(name="css")
        Skill.objects.create(name="java")

    def test_skill_query(self):
        response = self.query(
            '''
            query{
               skills{
                    name
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = Skill.objects.all().count()
        self.assertEqual(
            3,
            num_entries
        )

        # Test ordering

        self.assertEqual(
            content['data'].get('skills')[0].get('name'),
            'css'
        )
        self.assertEqual(
            content['data'].get('skills')[1].get('name'),
            'java'
        )
        self.assertEqual(
            content['data'].get('skills')[2].get('name'),
            'php'
        )
