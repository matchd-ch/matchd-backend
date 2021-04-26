import pytest

from db.models import FAQCategory


def faq_categories_query():
    return '''
    query {
        faqCategories {
            id
            name
        }
    }
    '''


@pytest.fixture
def faq_category_objects():
    return [
        FAQCategory.objects.create(id=1, name='Second category'),
        FAQCategory.objects.create(id=2, name='First category')
    ]


@pytest.fixture
def query_faq_categories(execute):
    def closure(user):
        return execute(faq_categories_query(), **{'user': user})
    return closure
