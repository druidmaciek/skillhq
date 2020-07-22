from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Resource
from .serializers import ResourceSerializer, TaskSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ResourceSerializer

    def get_queryset(self):
        user = self.request.user
        return Resource.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        tasks = request.data['tasks']
        #request.data['user'] = self.request.user.id
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            resource = serializer.save(user=request.user)

            #response = super(ResourceViewSet, self).create(request, *args, **kwargs)

            for task in tasks:
                task['resource'] = resource.id
                task_obj = TaskSerializer(data=task)
                if task_obj.is_valid():
                    task_obj.save()

            return Response(status=201, data={'msg': 'created'})
        return Response(status=400, data={'msg': serializer.error_messages})