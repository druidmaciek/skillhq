from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('resources/', views.resources_list, name='resource_list'),
    path("resource/<int:rid>/", views.resource_detail, name="resource_details"),
    path("notes/new/", views.new_note, name='new_note'),
    path("notes/<int:note_id>/", views.note_detail, name="note_detail"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
