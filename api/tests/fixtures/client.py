import pytest
from graphene.test import Client

from django.test import RequestFactory

from api.schema import schema


@pytest.fixture
def execute():

    def closure(query, variables=None, **kwargs):
        request_factory = RequestFactory()
        context_value = request_factory.get('/graphql/')
        user = kwargs.get('user')
        if user is not None:
            context_value.user = user
        response = Client(schema).execute(query,
                                          variable_values=variables,
                                          context_value=context_value)
        data = response.get('data')
        errors = response.get('errors')
        return data, errors

    return closure
