from rest_framework import serializers

from ..models import Resource, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'status', 'resource')


class ResourceSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = ('id', 'title', 'subject', 'resource_type', 'url',
                  'status', 'tasks', 'description')
