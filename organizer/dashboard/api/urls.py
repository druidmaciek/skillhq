from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("resources", views.ResourceViewSet, basename='resource')
router.register("tasks", views.TaskViewSet, basename='task')
router.register("notes", views.NotesViewSet, basename='note')
router.register("goals", views.GoalsViewSet, basename='goal')
router.register("posts", views.PostsViewSet, basename='post')
router.register("comments", views.CommentsViewSet, basename='comments')

app_name = "dashboard"
urlpatterns = [
    path("", include(router.urls)),
]
