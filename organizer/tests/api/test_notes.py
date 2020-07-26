import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from ..utils import create_user
from dashboard.models import Note, Resource
from dashboard.api.views import NotesViewSet


factory = APIRequestFactory()
note_detail = NotesViewSet.as_view(actions={'get': 'retrieve'})


@pytest.mark.django_db
def test_note_view_set_can_retrieve_owned(client):
    user = create_user()

    resource = Resource.objects.create(title="test",
                                       subject='test',
                                       user=user)
    note = Note.objects.create(title='test note', content="test content",
                               resource=resource)

    request = factory.get(reverse('api:note-detail', args=(note.pk,)))
    force_authenticate(request, user=user)
    resp = note_detail(request, pk=note.pk)

    assert resp.status_code == 200
