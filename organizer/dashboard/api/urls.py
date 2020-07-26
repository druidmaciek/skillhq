from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("resources", views.ResourceViewSet, basename='resource')
router.register("tasks", views.TaskViewSet, basename='task')
router.register("notes", views.NotesViewSet, basename='note')
router.register("goals", views.GoalsViewSet, basename='goal')
router.register("posts", views.PostsViewSet)
router.register("comments", views.CommentsViewSet)

app_name = "dashboard"
urlpatterns = [
    path("", include(router.urls)),
]
