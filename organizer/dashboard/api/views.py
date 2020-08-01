from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages

from ..models import Resource, Note, Task, Goal, Post, Comment, Subject
from .serializers import ResourceSerializer, \
    TaskSerializer, NoteSerializer, GoalSerializer, \
    PostSerializer, CommentSerializer
from actions.utils import create_action

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


            # Add valid tasks
            for task in tasks:
                task["resource"] = resource.id
                task_obj = TaskSerializer(data=task)
                if task_obj.is_valid():
                    task_obj.save()

            # Add subject
            try:
                subject = Subject.objects.get(name=resource.subject)
            except Subject.DoesNotExist:
                subject = Subject.objects.create(name=resource.subject)
            subject.users.add(request.user)
            subject.save()

            messages.success(request, f'"{resource.title}" added to your collection.')

            return Response(
                status=201, data={"msg": "created", "data": serializer.data}
            )
        # TODO show exact error message
        messages.error(request, f'Error occurred.')
        return Response(status=400, data={"msg": serializer.error_messages})

    def destroy(self, request, *args, **kwargs):
        response = super(ResourceViewSet, self).destroy(request, *args, **kwargs)
        messages.success(request, 'Resource Deleted.')
        return response


class TaskViewSet(BaseViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(resource__user=user)

    def partial_update(self, request, pk=None):
        response = super(TaskViewSet, self).partial_update(request, pk)
        if response.status_code == 200:
            if request.data['status'] and request.data['status'] == 'completed':
                create_action(request.user, 'completed a task')
        return response


class NotesViewSet(BaseViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(resource__user=user)


class GoalsViewSet(BaseViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def get_queryset(self):
        user = self.request.user
        return Goal.objects.filter(user=user)


class PostsViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        response = super(PostsViewSet, self).destroy(request, *args, **kwargs)
        messages.success(request, 'Post Deleted.')
        return response


class CommentsViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        response = super(CommentsViewSet, self).destroy(request, *args, **kwargs)
        messages.success(request, 'Comment Deleted.')
        return response
