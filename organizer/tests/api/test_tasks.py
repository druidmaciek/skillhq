import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from ..utils import create_user
from dashboard.models import Task, Resource
from dashboard.api.views import TaskViewSet


factory = APIRequestFactory()
task_detail = TaskViewSet.as_view(actions={'get': 'retrieve'})


@pytest.mark.django_db
def test_task_view_set_can_retrieve_owned(client):
    user = create_user()

    resource = Resource.objects.create(title="test",
                                       subject='test',
                                       user=user)
    task = Task.objects.create(title='test task', resource=resource)

    request = factory.get(reverse('api:task-detail', args=(task.pk,)))
    force_authenticate(request, user=user)
    resp = task_detail(request, pk=task.pk)

    assert resp.status_code == 200
