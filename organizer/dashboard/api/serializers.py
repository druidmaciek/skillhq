from rest_framework import serializers

from ..models import Resource, Task, Note, Goal, Post, Comment


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ("title", "subject")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "status", "resource", "updated", "created", "id")


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("title", "content", "resource", "updated", "created", 'id')


class ResourceSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = (
            "id",
            "title",
            "subject",
            "resource_type",
            "url",
            "status",
            "tasks",
            "description",
            "notes",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'content', 'comments')
