import pytest

from db.models.language import Language


@pytest.mark.django_db
def test_create_language(language_valid_args):
    language = Language.objects.create(**language_valid_args)

    assert isinstance(language, Language)


@pytest.mark.django_db
def test_get_language(language_valid_args):
    language = Language.objects.create(**language_valid_args)
    language = Language.objects.get(id=language.id)

    assert isinstance(language, Language)
    assert isinstance(language.name, str)

    assert language.name == language_valid_args.get('name')


@pytest.mark.django_db
def test_update_language(language_valid_args):
    new_name = 'Italian'
    language = Language.objects.create(**language_valid_args)
    Language.objects.filter(id=language.id).update(name=new_name)
    language.refresh_from_db()

    assert isinstance(language, Language)
    assert isinstance(language.name, str)

    assert language.name == new_name


@pytest.mark.django_db
def test_delete_language(language_valid_args):
    language = Language.objects.create(**language_valid_args)
    number_of_deletions, _ = language.delete()

    assert number_of_deletions == 1
