import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from ..utils import create_user
from dashboard.models import Goal, Resource
from dashboard.api.views import GoalsViewSet


factory = APIRequestFactory()
goal_detail = GoalsViewSet.as_view(actions={'get': 'retrieve'})


@pytest.mark.django_db
def test_goal_view_set_can_retrieve_owned(client):
    user = create_user()
    goal = Goal.objects.create(title='test goal', subject="test content",
                               user=user)

    request = factory.get(reverse('api:goal-detail', args=(goal.pk,)))
    force_authenticate(request, user=user)
    resp = goal_detail(request, pk=goal.pk)

    assert resp.status_code == 200
