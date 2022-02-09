import pytest

from db.models.faq_category import FAQCategory


@pytest.mark.django_db
def test_create_faq_category(faq_category_valid_args):
    faq_category = FAQCategory.objects.create(**faq_category_valid_args)

    assert isinstance(faq_category, FAQCategory)


@pytest.mark.django_db
def test_get_faq_category(faq_category_valid_args):
    faq_category = FAQCategory.objects.create(**faq_category_valid_args)
    faq_category = FAQCategory.objects.get(id=faq_category.id)

    assert isinstance(faq_category, FAQCategory)
    assert isinstance(faq_category.name, str)

    assert faq_category.name == faq_category_valid_args.get('name')


@pytest.mark.django_db
def test_update_faq_category(faq_category_valid_args):
    new_name = 'General questions'
    faq_category = FAQCategory.objects.create(**faq_category_valid_args)
    FAQCategory.objects.filter(id=faq_category.id).update(name=new_name)
    faq_category.refresh_from_db()

    assert isinstance(faq_category, FAQCategory)
    assert isinstance(faq_category.name, str)

    assert faq_category.name == new_name


@pytest.mark.django_db
def test_delete_faq_category(faq_category_valid_args):
    faq_category = FAQCategory.objects.create(**faq_category_valid_args)
    number_of_deletions, _ = faq_category.delete()

    assert number_of_deletions == 1
