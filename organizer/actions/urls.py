from django.urls import path

from . import views

app_name = 'actions'
urlpatterns = [
    path('like/', views.action_like, name='action_like'),
]