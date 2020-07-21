from rest_framework import serializers

from ..models import Resource, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'status')


class ResourceSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(required=False)

    class Meta:
        model = Resource
        fields = ('title', 'subject', 'resource_type', 'url',
                  'status')