import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from ..utils import create_user
from dashboard.models import Post, Resource
from dashboard.api.views import PostsViewSet


factory = APIRequestFactory()
post_detail = PostsViewSet.as_view(actions={'get': 'retrieve'})


@pytest.mark.django_db
def test_post_view_set_can_retrieve_owned(client):
    user = create_user()
    post = Post.objects.create(title='test post', content="test content",
                               user=user)

    request = factory.get(reverse('api:post-detail', args=(post.pk,)))
    force_authenticate(request, user=user)
    resp = post_detail(request, pk=post.pk)

    assert resp.status_code == 200
