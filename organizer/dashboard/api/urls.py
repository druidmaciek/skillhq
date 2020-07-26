from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("resources", views.ResourceViewSet, basename='resource')
router.register("tasks", views.TaskViewSet)
router.register("notes", views.NotesViewSet)
router.register("goals", views.GoalsViewSet)
router.register("posts", views.PostViewSet)
router.register("comments", views.CommentViewSet)

app_name = "dashboard"
urlpatterns = [
    path("", include(router.urls)),
]
