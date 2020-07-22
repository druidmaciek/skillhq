from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("resources", views.ResourceViewSet)
router.register("tasks", views.TaskViewSet)
router.register("notes", views.NotesViewSet)

app_name = "dashboard"
urlpatterns = [
    path("", include(router.urls)),
]
