import pytest
import requests

from account.forms import UserRegistrationForm
from account.models import Profile
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.urls import reverse

from ..utils import create_user, create_user_profile


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


@pytest.mark.django_db
def test_user_profile_creation():
    user = create_user()
    profile = create_user_profile(user)

    assert isinstance(profile, Profile)
    assert str(profile) == "Profile for user user"


@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse("account:register")
    resp = client.get(url)

    assert resp.status_code == 200


@pytest.mark.django_db
def test_register_view_post_success(client):
    url = reverse("account:register")
    resp = client.post(url,
                       data={
                           'username': 'johnny',
                           'email': 'email@email.com',
                           'password': 'hello199',
                           'password2': 'hello199'
                       })

    soup = BeautifulSoup(resp.content, 'html.parser')
    header = soup.find('h2').text

    assert 'Welcome johnny!' in header
    assert resp.status_code == 200


@pytest.mark.django_db
def test_register_view_post_form_invalid(client):
    url = reverse("account:register")
    resp = client.post(url,
                       data={
                           'username': 'johnny',
                           'email': 'email@email.com',
                           'password': 'hello199',
                           'password2': 'diffpassword'
                       })

    soup = BeautifulSoup(resp.content, 'html.parser')
    header = soup.find('ul', {'class': 'errorlist'}).text

    assert "Passwords don't match." in header
    assert resp.status_code == 200


@pytest.mark.django_db
def test_edit_profile_view_get(client):
    user = create_user(username='bill')
    profile = create_user_profile(user, about='I like tests')

    client.login(username='bill', password='Password123!')

    url = reverse("account:edit")
    resp = client.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    textarea = soup.find('textarea', {'name': 'about'}).text
    username = soup.find('input', {'id': 'username'})['value']

    assert resp.status_code == 200
    assert 'I like tests' in textarea
    assert 'bill' == username


@pytest.mark.django_db
def test_edit_profile_view_post_success(client):
    user = create_user(username='bill', email='different@email.com')
    profile = create_user_profile(user)

    client.login(username='bill', password='Password123!')
    url = reverse("account:edit")
    resp = client.post(url, data={
        'username': user.username,
        'email': user.email,
        'about': "I like unittests",
    })
    soup = BeautifulSoup(resp.content, 'html.parser')
    textarea = soup.find('textarea', {'name': 'about'}).text
    username = soup.find('input', {'id': 'username'})['value']

    assert resp.status_code == 200
    assert 'I like unittests' in textarea
    assert 'bill' == username


@pytest.mark.django_db
def test_edit_profile_view_post_form_invalid(client):
    create_user_profile(create_user(username='bill'))
    user = create_user()
    profile = create_user_profile(user)

    client.login(username=user.username, password='Password123!')
    url = reverse("account:edit")
    resp = client.post(url, data={
        'username': 'bill',
        'email': user.email,
        'about': "I like unittests",
    })
    soup = BeautifulSoup(resp.content, 'html.parser')
    alert = soup.find('div', {'id': 'alerts'}).text

    assert resp.status_code == 200
    assert 'Error updating profile...' in alert
