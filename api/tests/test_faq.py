import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_faqs, faq_objects, login, user_student):
    login(user_student)
    data, errors = query_faqs(user_student, 'company-1')
    assert errors is None
    assert data is not None

    objects = data.get('companyFaqs')
    assert objects is not None
    assert len(objects) == len(faq_objects)
    first_faq = objects[0]
    assert first_faq.get('name') == faq_objects[0].category.name
    assert first_faq.get('faqs')[0].get('id') == faq_objects[0].id
    assert first_faq.get('faqs')[0].get('question') == faq_objects[0].question
    assert first_faq.get('faqs')[0].get('answer') == faq_objects[0].answer


@pytest.mark.django_db
def test_add_faq_valid(faq_add_faq, login, user_employee, faq_category_objects):
    login(user_employee)
    data, errors = faq_add_faq(user_employee, faq_category_objects[0].id, 'FAQ Question', 'FAQ Answer')
    assert errors is None
    assert data is not None
    assert data.get('addFaq') is not None
    assert data.get('addFaq').get('success') is True

    errors = data.get('addFaq').get('errors')
    assert errors is None


@pytest.mark.django_db
def test_add_faq_too_long(faq_add_faq, login, user_employee, faq_category_objects):
    login(user_employee)
    data, errors = faq_add_faq(user_employee, faq_category_objects[0].id, 'A'*10000, 'B'*10000)
    assert errors is None
    assert data is not None
    assert data.get('addFaq') is not None
    assert data.get('addFaq').get('success') is False

    errors = data.get('addFaq').get('errors')
    assert errors is not None
    assert 'question' in errors
    assert 'answer' in errors


@pytest.mark.django_db
def test_add_faq_valid_without_login(faq_add_faq, faq_category_objects):
    data, errors = faq_add_faq(AnonymousUser(), faq_category_objects[0].id, 'FAQ Question', 'FAQ Answer')
    assert errors is not None
    assert data is not None
    assert data.get('addFaq') is None


@pytest.mark.django_db
def test_add_faq_invalid(faq_add_faq, login, user_employee, faq_category_objects):
    login(user_employee)
    data, errors = faq_add_faq(user_employee, faq_category_objects[1].id, '', '')
    assert errors is None
    assert data is not None
    assert data.get('addFaq') is not None
    assert data.get('addFaq').get('success') is not True

    errors = data.get('addFaq').get('errors')

    assert 'question' in errors
    assert 'answer' in errors


@pytest.mark.django_db
def test_add_faq_invalid_category(faq_add_faq, login, user_employee):
    login(user_employee)
    data, errors = faq_add_faq(user_employee, 1337, 'Question', 'Answer')
    assert errors is None
    assert data is not None
    assert data.get('addFaq') is not None
    assert data.get('addFaq').get('success') is False
    assert data.get('addFaq').get('errors') is not None


@pytest.mark.django_db
def test_update_faq_valid(faq_update_faq, login, user_employee, faq_objects, faq_category_objects):
    login(user_employee)
    data, errors = faq_update_faq(user_employee, faq_objects[0].id, faq_category_objects[1].id, 'New Question',
                                  'New Answer')
    assert errors is None
    assert data is not None
    assert data.get('updateFaq') is not None
    assert data.get('updateFaq').get('success') is True

    company = get_user_model().objects.get(pk=user_employee.id).company
    updated_faq = company.faqs.all()[0]
    assert updated_faq.category.name == faq_category_objects[1].name
    assert updated_faq.id == faq_objects[0].id
    assert updated_faq.question == 'New Question'
    assert updated_faq.answer == 'New Answer'

    errors = data.get('updateFaq').get('errors')
    assert errors is None


@pytest.mark.django_db
def test_update_faq_valid_without_login(faq_update_faq, faq_category_objects, faq_objects):
    data, errors = faq_update_faq(AnonymousUser(), faq_objects[0].id, faq_category_objects[1].id, 'New Question',
                                  'New Answer')
    assert errors is not None
    assert data is not None
    assert data.get('updateFaq') is None


@pytest.mark.django_db
def test_update_faq_too_long(faq_update_faq, login, user_employee, faq_objects, faq_category_objects):
    login(user_employee)
    data, errors = faq_update_faq(user_employee, faq_objects[0].id, faq_category_objects[1].id, 'a'*10000, 'b'*10000)
    assert errors is None
    assert data is not None
    assert data.get('updateFaq') is not None
    assert data.get('updateFaq').get('success') is False

    company = get_user_model().objects.get(pk=user_employee.id).company
    updated_faq = company.faqs.all()[0]
    assert updated_faq.category.name == faq_objects[0].category.name
    assert updated_faq.id == faq_objects[0].id
    assert updated_faq.question == 'Old Question'
    assert updated_faq.answer == 'Old Answer'

    errors = data.get('updateFaq').get('errors')
    assert errors is not None
    assert 'question' in errors
    assert 'answer' in errors


@pytest.mark.django_db
def test_update_faq_invalid(faq_update_faq, login, user_employee, faq_objects, faq_category_objects):
    login(user_employee)
    data, errors = faq_update_faq(user_employee, faq_objects[0].id, faq_category_objects[1].id, '', '')
    assert errors is None
    assert data is not None
    assert data.get('updateFaq') is not None
    assert data.get('updateFaq').get('success') is False

    company = get_user_model().objects.get(pk=user_employee.id).company
    updated_faq = company.faqs.all()[0]
    assert updated_faq.category.name == faq_objects[0].category.name
    assert updated_faq.id == faq_objects[0].id
    assert updated_faq.question == 'Old Question'
    assert updated_faq.answer == 'Old Answer'

    errors = data.get('updateFaq').get('errors')
    assert errors is not None
    assert 'question' in errors
    assert 'answer' in errors


@pytest.mark.django_db
def test_update_faq_invalid_faq_id(faq_update_faq, login, user_employee, faq_objects, faq_category_objects):
    login(user_employee)
    data, errors = faq_update_faq(user_employee, 1337, faq_category_objects[1].id, 'New Question', 'New Answer')
    assert errors is None
    assert data is not None
    assert data.get('updateFaq').get('success') is False

    company = get_user_model().objects.get(pk=user_employee.id).company
    updated_faq = company.faqs.all()[0]
    assert updated_faq.category.name == faq_category_objects[0].name
    assert updated_faq.id == faq_objects[0].id
    assert updated_faq.question == 'Old Question'
    assert updated_faq.answer == 'Old Answer'

    errors = data.get('updateFaq').get('errors')
    assert errors is not None


@pytest.mark.django_db
def test_update_faq_invalid_faq_id(faq_update_faq, login, user_employee, faq_objects, faq_category_objects):
    login(user_employee)
    data, errors = faq_update_faq(user_employee, faq_objects[0].id, 1337, 'New Question', 'New Answer')
    assert errors is None
    assert data is not None
    assert data.get('updateFaq') is not None
    assert data.get('updateFaq').get('success') is False

    company = get_user_model().objects.get(pk=user_employee.id).company
    updated_faq = company.faqs.all()[0]
    assert updated_faq.category.name == faq_category_objects[0].name
    assert updated_faq.id == faq_objects[0].id
    assert updated_faq.question == 'Old Question'
    assert updated_faq.answer == 'Old Answer'

    errors = data.get('updateFaq').get('errors')
    assert errors is not None


@pytest.mark.django_db
def test_delete_faq_valid(faq_delete_faq, login, user_employee, faq_objects):
    login(user_employee)
    data, errors = faq_delete_faq(user_employee, faq_objects[0].id)
    assert errors is None
    assert data is not None
    assert data.get('deleteFaq') is not None
    assert data.get('deleteFaq').get('success') is True

    company = get_user_model().objects.get(pk=user_employee.id).company
    delete_faq = company.faqs.all()
    assert len(delete_faq) == len(faq_objects) - 1

    errors = data.get('deleteFaq').get('errors')
    assert errors is None


@pytest.mark.django_db
def test_delete_faq_valid_without_login(faq_delete_faq, faq_objects):
    data, errors = faq_delete_faq(AnonymousUser(), faq_objects[0].id)
    assert errors is not None
    assert data is not None
    assert data.get('deleteFaq') is None


@pytest.mark.django_db
def test_delete_faq_invalid(faq_delete_faq, login, user_employee, faq_objects):
    login(user_employee)
    data, errors = faq_delete_faq(user_employee, 1337)
    assert errors is not None
    assert data is not None

    company = get_user_model().objects.get(pk=user_employee.id).company
    delete_faq = company.faqs.all()
    assert len(delete_faq) == len(faq_objects)
