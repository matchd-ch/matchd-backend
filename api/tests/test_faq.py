import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from api.tests.fixtures import user_employee


@pytest.mark.django_db
def test_query(query_faqs, faq_objects, login, user_student):
    login(user_student)
    data, errors = query_faqs(user_student, 'company-1')
    assert errors is None
    assert data is not None

    objects = data.get('companyFaqs')
    assert objects is not None
    assert len(objects) == len(faq_objects)
    assert objects[0].get('name') == 'Second category'
    assert objects[0].get('faqs')[0].get('id') == '1'
    assert objects[0].get('faqs')[0].get('title') == 'Old Title'
    assert objects[0].get('faqs')[0].get('question') == 'Old Question'
    assert objects[0].get('faqs')[0].get('answer') == 'Old Answer'


@pytest.mark.django_db
def test_add_faq_valid(faq_add_faq, login, user_employee, faq_category_objects):
    login(user_employee)
    data, errors = faq_add_faq(user_employee, faq_category_objects[0].id, 'FAQ Title', 'FAQ Question', 'FAQ Answer')
    assert errors is None
    assert data is not None
    assert data.get('addFaq') is not None
    assert data.get('addFaq').get('success') is True

    errors = data.get('addFaq').get('errors')
    assert errors is None


@pytest.mark.django_db
def test_add_faq_invalid(faq_add_faq, login, user_employee, faq_category_objects):
    login(user_employee)
    data, errors = faq_add_faq(user_employee, faq_category_objects[1].id, '', '', '')
    assert errors is  None
    assert data is not None
    assert data.get('addFaq') is not None
    assert data.get('addFaq').get('success') is not True

    errors = data.get('addFaq').get('errors')

    assert 'title' in errors
    assert 'question' in errors
    assert 'answer' in errors


@pytest.mark.django_db
def test_update_faq_valid(faq_update_faq, login, user_employee, faq_objects, faq_category_objects):
    login(user_employee)
    data, errors = faq_update_faq(user_employee, faq_objects[0].id, faq_category_objects[1].id, 'New Title', 'New Question', 'New Answer')
    assert errors is None
    assert data is not None
    assert data.get('updateFaq') is not None
    assert data.get('updateFaq').get('success') is True

    company = get_user_model().objects.get(pk=user_employee.id).company
    updated_faq = company.faqs.all()[0]
    assert updated_faq.category.name == 'First category'
    assert updated_faq.id == 1
    assert updated_faq.title == 'New Title'
    assert updated_faq.question == 'New Question'
    assert updated_faq.answer == 'New Answer'

    errors = data.get('updateFaq').get('errors')
    assert errors is None


@pytest.mark.django_db
def test_update_faq_invalid(faq_update_faq, login, user_employee, faq_objects, faq_category_objects):
    login(user_employee)
    data, errors = faq_update_faq(user_employee, faq_objects[0].id, faq_category_objects[1].id, '', '', '')
    assert errors is None
    assert data is not None
    assert data.get('updateFaq') is not None
    assert data.get('updateFaq').get('success') is False

    company = get_user_model().objects.get(pk=user_employee.id).company
    updated_faq = company.faqs.all()[0]
    assert updated_faq.category.name == 'Second category'
    assert updated_faq.id == 1
    assert updated_faq.title == 'Old Title'
    assert updated_faq.question == 'Old Question'
    assert updated_faq.answer == 'Old Answer'

    errors = data.get('updateFaq').get('errors')
    assert errors is not None
    assert 'title' in errors
    assert 'question' in errors
    assert 'answer' in errors