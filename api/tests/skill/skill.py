import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import Skill, skill


class SkillGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpTestData(cls):
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
        self.assertEqual(
            content['data'].get('skills')[0].get('name'),
            'php'
        )
        self.assertEqual(
            content['data'].get('skills')[1].get('name'),
            'css'
        )
        self.assertEqual(
            content['data'].get('skills')[2].get('name'),
            'java'
        )
