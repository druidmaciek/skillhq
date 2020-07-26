import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from ..utils import create_user
from dashboard.models import Comment, Post
from dashboard.api.views import CommentsViewSet

factory = APIRequestFactory()
comment_detail = CommentsViewSet.as_view(actions={'get': 'retrieve'})


@pytest.mark.django_db
def test_comment_view_set_can_retrieve_owned(client):
    user = create_user()

    post = Post.objects.create(title="test",
                               content='test',
                               user=user)
    comment = Comment.objects.create(content='test comment', post=post,
                                     user=user)

    request = factory.get(reverse('api:comment-detail', args=(comment.pk,)))
    force_authenticate(request, user=user)
    resp = comment_detail(request, pk=comment.pk)

    assert resp.status_code == 200
