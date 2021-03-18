import json
from graphene_django.utils import GraphQLTestCase

from api.schema import schema
from db.models import SoftSkill


class SoftSkillGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        SoftSkill.objects.create(id=1, student="I like working", company='You like working')
        SoftSkill.objects.create(id=2, student="I like things", company='You like things')

    def test_soft_skill_query(self):
        response = self.query(
            '''
            query{
               softSkills{
                    id
                    student
                    company
                  }
              }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        num_entries = SoftSkill.objects.all().count()
        self.assertEqual(
            2,
            num_entries
        )

        self.assertEqual(
            content['data'].get('softSkills')[0].get('company'),
            'You like working'
        )
        self.assertEqual(
            content['data'].get('softSkills')[0].get('student'),
            'I like working'
        )
        self.assertEqual(
            content['data'].get('softSkills')[1].get('company'),
            'You like things'
        )
        self.assertEqual(
            content['data'].get('softSkills')[1].get('student'),
            'I like things'
        )
