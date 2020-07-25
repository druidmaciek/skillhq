import pytest
import requests

from account.forms import UserRegistrationForm
from account.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy


BASE_URL = 'http://127.0.0.1:8000'

@pytest.mark.django_db
def test_register_form_success():
    form_data = {
        'username': 'druid',
        'email': 'email@email.com',
        'password': 'pass123',
        'password2': 'pass123',
    }
    form = UserRegistrationForm(data=form_data)

    assert form.is_valid() is True


@pytest.mark.django_db
def test_register_form_wrong_pass():
    form_data = {
        'username': 'druid',
        'email': 'email@email.com',
        'password': 'pass123',
        'password2': 'totalydifferentpassword'
    }
    form = UserRegistrationForm(data=form_data)

    assert form.is_valid() is False


def create_user(username='user', email='email@email.com'):
    user = User.objects.create_user(username=username,
                                    email=email)
    return user


def create_user_profile(user):
    profile = Profile.objects.create(user=user)
    return profile


@pytest.mark.django_db
def test_user_profile_creation():
    user = create_user()
    profile = create_user_profile(user)

    assert isinstance(profile, Profile)
    assert str(profile) == "Profile for user user"


# @pytest.mark.django_db
# def test_register_view_get(client):
#     url = reverse("account:register")
#     resp = client.get(url)
#
#     assert resp.status_code == 200
#
#
# @pytest.mark.django_db
# def test_register_view_post(client):
#     url = reverse("account:register")
#     resp = client.post(url,
#                          data={
#                              'username': 'johnny',
#                              'email': 'email@email.com',
#                              'password': 'hello199',
#                              'password2': 'hello199'
#                          })
#
#     assert resp.status_code == 200
