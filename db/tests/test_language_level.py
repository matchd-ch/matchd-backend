import pytest

from db.models.language_level import LanguageLevel


@pytest.mark.django_db
def test_create_language_level(language_level_valid_args):
    language_level = LanguageLevel.objects.create(**language_level_valid_args)

    assert isinstance(language_level, LanguageLevel)


@pytest.mark.django_db
def test_get_language_level(language_level_valid_args):
    language_level = LanguageLevel.objects.create(**language_level_valid_args)
    language_level = LanguageLevel.objects.get(id=language_level.id)

    assert isinstance(language_level, LanguageLevel)
    assert isinstance(language_level.level, str)

    assert language_level.level == language_level_valid_args.get('level')
    assert language_level.description == language_level_valid_args.get('description')
    assert language_level.value == language_level_valid_args.get('value')


@pytest.mark.django_db
def test_update_language_level(language_level_valid_args):
    new_level = 'C1+'
    language_level = LanguageLevel.objects.create(**language_level_valid_args)
    LanguageLevel.objects.filter(id=language_level.id).update(level=new_level)
    language_level.refresh_from_db()

    assert isinstance(language_level, LanguageLevel)
    assert isinstance(language_level.level, str)

    assert language_level.level == new_level


@pytest.mark.django_db
def test_delete_language_level(language_level_valid_args):
    language_level = LanguageLevel.objects.create(**language_level_valid_args)
    number_of_deletions, _ = language_level.delete()

    assert number_of_deletions == 1
