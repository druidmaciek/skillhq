from rest_framework import generics
from rest_framework.authentication import BasicAuthentication

from ..models import Resource, Task
from .serializers import ResourceSerializer, TaskSerializer



class ResourceListView(generics.ListAPIView):
    authentication_classes = (BasicAuthentication,)
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ResourceDetailView(generics.RetrieveAPIView):
    authentication_classes = (BasicAuthentication,)
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class TaskListView(generics.ListAPIView):
    authentication_classes = (BasicAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveAPIView):
    authentication_classes = (BasicAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer