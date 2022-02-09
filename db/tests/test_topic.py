import pytest

from db.models.topic import Topic


@pytest.mark.django_db
def test_create_topic(topic_valid_args):
    topic = Topic.objects.create(**topic_valid_args)

    assert isinstance(topic, Topic)


@pytest.mark.django_db
def test_get_topic(topic_valid_args):
    topic = Topic.objects.create(**topic_valid_args)
    topic = Topic.objects.get(id=topic.id)

    assert isinstance(topic, Topic)
    assert isinstance(topic.name, str)

    assert topic.name == topic_valid_args.get('name')


@pytest.mark.django_db
def test_update_topic(topic_valid_args):
    new_name = 'erlang'
    topic = Topic.objects.create(**topic_valid_args)
    Topic.objects.filter(id=topic.id).update(name=new_name)
    topic.refresh_from_db()

    assert isinstance(topic, Topic)
    assert isinstance(topic.name, str)

    assert topic.name == new_name


@pytest.mark.django_db
def test_delete_topic(topic_valid_args):
    topic = Topic.objects.create(**topic_valid_args)
    number_of_deletions, _ = topic.delete()

    assert number_of_deletions == 1
