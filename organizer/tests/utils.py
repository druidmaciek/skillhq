from django.contrib.auth.models import User

from account.models import Profile

def create_user(username='user', email='email@email.com'):
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password='Password123!')
    return user


def create_user_profile(user, about=None):
    profile = Profile.objects.create(user=user, about=about)
    return profile