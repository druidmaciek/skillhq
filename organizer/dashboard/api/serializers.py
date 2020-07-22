from rest_framework import serializers

from ..models import Resource, Task, Note


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'status', 'resource', 'updated', 'created', 'id')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'content', 'resource', 'updated', 'created')


class ResourceSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = ('id', 'title', 'subject', 'resource_type', 'url',
                  'status', 'tasks', 'description', 'notes')
