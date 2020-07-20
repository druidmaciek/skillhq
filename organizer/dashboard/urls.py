from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('addResource/', views.add_resource, name='add_resource'),
    path('resource/<int:rid>/',
         views.resource_detail,
         name='resource_details')
]