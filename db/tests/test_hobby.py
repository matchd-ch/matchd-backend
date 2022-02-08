import pytest

from db.models.hobby import Hobby
from db.models.student import Student


@pytest.mark.django_db
def test_create_hobby(hobby_valid_args):
    hobby = Hobby.objects.create(**hobby_valid_args)

    assert isinstance(hobby, Hobby)


@pytest.mark.django_db
def test_get_hobby(hobby_valid_args):
    hobby = Hobby.objects.create(**hobby_valid_args)
    hobby = Hobby.objects.get(id=hobby.id)

    assert isinstance(hobby, Hobby)
    assert isinstance(hobby.name, str)
    assert isinstance(hobby.student, Student)

    assert hobby.name == hobby_valid_args.get('name')
    assert hobby.student.city == hobby_valid_args.get('student').city
    assert hobby.student.slug == hobby_valid_args.get('student').slug


@pytest.mark.django_db
def test_update_hobby(hobby_valid_args):
    new_name = 'running'
    hobby = Hobby.objects.create(**hobby_valid_args)
    Hobby.objects.filter(id=hobby.id).update(name=new_name)
    hobby.refresh_from_db()

    assert isinstance(hobby, Hobby)
    assert isinstance(hobby.name, str)

    assert hobby.name == new_name


@pytest.mark.django_db
def test_delete_hobby(hobby_valid_args):
    hobby = Hobby.objects.create(**hobby_valid_args)
    number_of_deletions, _ = hobby.delete()

    assert number_of_deletions == 1
