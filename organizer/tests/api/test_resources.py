import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from dashboard.api.views import ResourceViewSet
from dashboard.models import Resource

from ..utils import create_user, create_user_profile

factory = APIRequestFactory()
resource_detail = ResourceViewSet.as_view(actions={'get': 'retrieve'})
resource_list = ResourceViewSet.as_view(actions={'post': 'create'})
resource_delete = ResourceViewSet.as_view(actions={'delete': 'destroy'})
RESOURCE_DATA = {
    "title": "Test Resource",
    "subject": "test subject",
    "tasks": [
        {
            "title": "test task"
        },
        {
            "title": "2nd Task"
        }
    ]
}


def mock_messages(request):
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)


@pytest.mark.django_db
def test_resource_view_set_can_retrieve_owned(client):
    user = create_user()

    resource = Resource.objects.create(title="test",
                                       subject='test',
                                       user=user)

    request = factory.get(reverse('api:resource-detail', args=(resource.pk,)))
    force_authenticate(request, user=user)
    resp = resource_detail(request, pk=resource.pk)

    assert resp.status_code == 200


@pytest.mark.django_db
def test_resource_view_set_cant_retrieve_non_owned(client):
    user = create_user()
    user2 = create_user(username='bill', email='email@email.com')

    resource = Resource.objects.create(title="test",
                                       subject='test',
                                       user=user)

    request = factory.get(reverse('api:resource-detail', args=(resource.pk,)))
    force_authenticate(request, user=user2)
    resp = resource_detail(request, pk=resource.pk)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_resource_view_set_create_success(client):
    user = create_user()

    request = factory.post(reverse('api:resource-list'), RESOURCE_DATA, format='json')
    mock_messages(request)
    force_authenticate(request, user=user)
    resp = resource_list(request)
    resource = Resource.objects.get(pk=resp.data['data']['id'])

    assert resp.status_code == 201
    assert resp.data['data']['title'] == 'Test Resource'
    assert len(resource.tasks.all()) == 2


@pytest.mark.django_db
def test_resource_view_set_create_failure_resource_invalid(client):
    user = create_user()
    data = RESOURCE_DATA.copy()
    data['url'] = 'incorrect url'

    request = factory.post(reverse('api:resource-list'), data, format='json')
    mock_messages(request)
    force_authenticate(request, user=user)
    resp = resource_list(request)
    print(resp.data, reverse('api:resource-list'), resp.status_code)

    assert resp.status_code == 400


@pytest.mark.django_db
def test_resource_view_set_create_success_task_invalid(client):
    """ Resource added, but the task on resource is invalid,
    so tasks are not added.
    """
    user = create_user()
    data = RESOURCE_DATA.copy()
    data['tasks'] = [{'tutle': 'wrong title key'}]

    request = factory.post(reverse('api:resource-list'), data, format='json')
    mock_messages(request)
    force_authenticate(request, user=user)
    resp = resource_list(request)
    resource = Resource.objects.get(pk=resp.data['data']['id'])

    assert resp.status_code == 201
    assert resp.data['data']['title'] == 'Test Resource'
    assert len(resource.tasks.all()) == 0


@pytest.mark.django_db
def test_resource_view_set_destroy_success(client):
    user = create_user()
    resource = Resource.objects.create(title="test",
                                       subject='test',
                                       user=user)

    request = factory.delete(reverse('api:resource-detail', args=(resource.pk,)))
    mock_messages(request)
    force_authenticate(request, user=user)
    resp = resource_delete(request, pk=resource.id)

    assert resp.status_code == 204
    assert Resource.objects.count() == 0


@pytest.mark.django_db
def test_resource_view_set_destroy_failure_deleting_other_users_resource(client):
    user = create_user()
    user2 = create_user(username='bill', email='email@email.com')
    resource = Resource.objects.create(title="test",
                                       subject='test',
                                       user=user2)

    request = factory.delete(reverse('api:resource-detail', args=(resource.pk,)))
    mock_messages(request)
    force_authenticate(request, user=user)
    resp = resource_delete(request, pk=resource.id)

    assert resp.status_code != 204
    assert Resource.objects.count() == 1


@pytest.mark.django_db
def test_resource_view_set_destroy_failure_delete_non_existing_resource(client):
    user = create_user()

    request = factory.delete(reverse('api:resource-detail', args=(999,)))
    mock_messages(request)
    force_authenticate(request, user=user)
    resp = resource_delete(request, pk=999)

    assert resp.status_code != 204
    assert Resource.objects.count() == 0
