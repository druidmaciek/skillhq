from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('resources/',
         views.ResourceListView.as_view(),
         name='resource_list'),
    path('resources/<pk>/',
         views.ResourceDetailView.as_view(),
         name='resource_detail'),
    path('tasks/',
         views.TaskListView.as_view(),
         name='task_list'),
    path('tasks/<pk>/',
         views.TaskDetailView.as_view(),
         name='task_detail'),
]
