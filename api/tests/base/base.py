from graphene_django.utils import GraphQLTestCase
from api.schema import schema


class BaseGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
