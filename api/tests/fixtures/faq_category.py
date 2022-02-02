import pytest

from graphql_relay import to_global_id

from db.models import FAQCategory


def faq_category_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on FAQCategory {
                name
            }
        }
    }
    '''


def faq_categories_query():
    return '''
    query {
        faqCategories {
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    id
                    name
                }
            }
        }
    }
    '''


@pytest.fixture
def faq_category_objects():
    return [
        FAQCategory.objects.create(id=1, name='First category'),
        FAQCategory.objects.create(id=2, name='Second category')
    ]


@pytest.fixture
def query_faq_category_node(execute):

    def closure(user, id_value):
        return execute(faq_category_node_query(),
                       variables={'id': to_global_id('FAQCategory', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_faq_categories(execute):

    def closure(user):
        return execute(faq_categories_query(), **{'user': user})

    return closure
