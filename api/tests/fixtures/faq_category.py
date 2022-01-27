import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import FAQCategory


def faq_category_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on FAQCategory {
                name
            }
        }
    }
    ''' % b64_encoded_id


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
    def closure(user, node_id):
        return execute(faq_category_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_faq_categories(execute):
    def closure(user):
        return execute(faq_categories_query(), **{'user': user})
    return closure
