import pytest

from ..utils import create_user
from dashboard.models import Resource, Task, Note, Goal, Post, Comment


@pytest.mark.django_db
def test_resource_creation():
    user = create_user()
    resource = Resource.objects.create(title='test resource',
                                       subject='test subject',
                                       user=user)

    assert isinstance(resource, Resource)
    assert str(resource) == "test resource"


@pytest.mark.django_db
def test_task_creation():
    user = create_user()
    resource = Resource.objects.create(title='test resource',
                                       subject='test subject',
                                       user=user)
    task = Task.objects.create(title='test task', resource=resource)

    assert isinstance(task, Task)
    assert str(task) == "test task"


@pytest.mark.django_db
def test_note_creation():
    user = create_user()
    resource = Resource.objects.create(title='test resource',
                                       subject='test subject',
                                       user=user)
    note = Note.objects.create(title='test note',
                               content='test',
                               resource=resource)

    assert isinstance(note, Note)
    assert str(note) == "test note"


@pytest.mark.django_db
def test_goal_creation():
    user = create_user()
    goal = Goal.objects.create(title='test goal',
                               subject='test subject',
                               user=user)

    assert isinstance(goal, Goal)
    assert str(goal) == "test goal"


@pytest.mark.django_db
def test_post_creation():
    user = create_user()
    post = Post.objects.create(title='test post',
                               content='test',
                               user=user)

    assert isinstance(post, Post)
    assert str(post) == "test post"


@pytest.mark.django_db
def test_comment_creation():
    user = create_user()
    post = Post.objects.create(title='test post',
                               content='test',
                               user=user)

    comment = Comment.objects.create(content='test', post=post,
                                  user=user)

    assert isinstance(comment, Comment)
    assert str(comment) == "Comment by user"
