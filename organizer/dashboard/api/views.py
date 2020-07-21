from rest_framework import generics

from ..models import Resource, Task
from .serializers import ResourceSerializer, TaskSerializer


class ResourceListView(generics.ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ResourceDetailView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer