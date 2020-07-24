from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages

from ..models import Resource, Note, Task
from .serializers import ResourceSerializer, TaskSerializer, NoteSerializer


class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ResourceViewSet(BaseViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_queryset(self):
        user = self.request.user
        return Resource.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        tasks = request.data["tasks"]
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            resource = serializer.save(user=request.user)

            for task in tasks:
                task["resource"] = resource.id
                task_obj = TaskSerializer(data=task)
                if task_obj.is_valid():
                    task_obj.save()

            messages.success(request, f'"{resource.title}" added to your collection.')

            return Response(
                status=201, data={"msg": "created", "data": serializer.data}
            )
        # TODO show exact error message
        messages.error(request, f'Error occurred.')
        return Response(status=400, data={"msg": serializer.error_messages})

    def destroy(self, request, *args, **kwargs):
        response = super(ResourceViewSet, self).destroy(request, *args, **kwargs)
        response.status_code
        if response.status_code == status.HTTP_204_NO_CONTENT:
            messages.success(request, 'Resource Deleted.')
        else:
            messages.error(request, 'There was a problem deleting this resource.')
        return response


class TaskViewSet(BaseViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(resource__user=user)


class NotesViewSet(BaseViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(resource__user=user)

