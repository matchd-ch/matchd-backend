import pytest

from db.models.language import Language
from db.models.language_level import LanguageLevel
from db.models.student import Student
from db.models.user_language_relation import UserLanguageRelation


@pytest.mark.django_db
def test_create_user_language_relation(user_language_relation_valid_args):
    user_language_relation = UserLanguageRelation.objects.create(
        **user_language_relation_valid_args)

    assert isinstance(user_language_relation, UserLanguageRelation)


@pytest.mark.django_db
def test_get_user_language_relation(user_language_relation_valid_args):
    user_language_relation = UserLanguageRelation.objects.create(
        **user_language_relation_valid_args)
    user_language_relation = UserLanguageRelation.objects.get(id=user_language_relation.id)

    assert isinstance(user_language_relation, UserLanguageRelation)
    assert isinstance(user_language_relation.student, Student)
    assert isinstance(user_language_relation.language, Language)
    assert isinstance(user_language_relation.language_level, LanguageLevel)

    assert user_language_relation.student == user_language_relation_valid_args.get('student')
    assert user_language_relation.language == user_language_relation_valid_args.get('language')
    assert user_language_relation.language_level == user_language_relation_valid_args.get(
        'language_level')


@pytest.mark.django_db
def test_update_user_language_relation(user_language_relation_valid_args, create_language):
    new_language = create_language('Italian')
    user_language_relation = UserLanguageRelation.objects.create(
        **user_language_relation_valid_args)
    UserLanguageRelation.objects.filter(id=user_language_relation.id).update(language=new_language)
    user_language_relation.refresh_from_db()

    assert isinstance(user_language_relation, UserLanguageRelation)
    assert isinstance(user_language_relation.language, Language)

    assert user_language_relation.language == new_language


@pytest.mark.django_db
def test_delete_user_language_relation(user_language_relation_valid_args):
    user_language_relation = UserLanguageRelation.objects.create(
        **user_language_relation_valid_args)
    number_of_deletions, _ = user_language_relation.delete()

    assert number_of_deletions == 1
