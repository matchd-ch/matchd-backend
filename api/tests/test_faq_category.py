import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_faq_categories, faq_category_objects):
    data, errors = query_faq_categories(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('faqCategories')
    assert objects is not None
    assert len(objects) == len(faq_category_objects)
    assert objects[0].get('name') == 'First category'
    assert objects[1].get('name') == 'Second category'
