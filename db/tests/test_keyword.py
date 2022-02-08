import pytest

from db.models.keyword import Keyword


@pytest.mark.django_db
def test_create_keyword(keyword_valid_args):
    keyword = Keyword.objects.create(**keyword_valid_args)

    assert isinstance(keyword, Keyword)


@pytest.mark.django_db
def test_get_keyword(keyword_valid_args):
    keyword = Keyword.objects.create(**keyword_valid_args)
    keyword = Keyword.objects.get(id=keyword.id)

    assert isinstance(keyword, Keyword)
    assert isinstance(keyword.name, str)

    assert keyword.name == keyword_valid_args.get('name')


@pytest.mark.django_db
def test_update_keyword(keyword_valid_args):
    new_name = 'two'
    keyword = Keyword.objects.create(**keyword_valid_args)
    Keyword.objects.filter(id=keyword.id).update(name=new_name)
    keyword.refresh_from_db()

    assert isinstance(keyword, Keyword)
    assert isinstance(keyword.name, str)

    assert keyword.name == new_name


@pytest.mark.django_db
def test_delete_keyword(keyword_valid_args):
    keyword = Keyword.objects.create(**keyword_valid_args)
    number_of_deletions, _ = keyword.delete()

    assert number_of_deletions == 1
