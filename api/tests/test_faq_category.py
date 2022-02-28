import pytest

from django.contrib.auth.models import AnonymousUser

from api.tests.helper.node_helper import assert_node_field, assert_node_id


@pytest.mark.django_db
def test_query(query_faq_categories, faq_category_objects):
    data, errors = query_faq_categories(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('faqCategories').get('edges')
    assert edges is not None
    assert len(edges) == len(faq_category_objects)
    assert_node_id(edges[0].get('node'), 'FAQCategory', faq_category_objects[0].id)
    assert_node_id(edges[1].get('node'), 'FAQCategory', faq_category_objects[1].id)
    assert_node_field(edges[0].get('node'), 'name', faq_category_objects[0].name)
    assert_node_field(edges[1].get('node'), 'name', faq_category_objects[1].name)


@pytest.mark.django_db
def test_node_query(query_faq_category_node, faq_category_objects):
    data, errors = query_faq_category_node(AnonymousUser(), faq_category_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'FAQCategory', faq_category_objects[0].id)
    assert_node_field(node, 'name', faq_category_objects[0].name)
