import pytest

from ..utils import create_user
from dashboard.models import Resource


@pytest.mark.django_db
def test_user_profile_creation():
    user = create_user()
    resource = Resource.objects.create(title='test resource',
                                       subject='test subject',
                                       user=user)

    assert isinstance(resource, Resource)
    assert str(resource) == "test resource"
