from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    STATUS_CHOICES = (
        ("Completed", "Completed"),
        ("In Progress", "In Progress"),
        ("Not Started/On Hold", "Not Started/On Hold"),
    )
    TYPE_CHOICES = (
        ("Video Course", "Video Course"),
        ("Text Course", "Text Course"),
        ("Text Tutorial", "Text Tutorial"),
        ("Video Tutorial", "Video Tutorial"),
        ("eBook", "eBook"),
        ("Book", "Book"),
        ("Newsletter", "Newsletter"),
        ("Other", "Other"),
    )
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, db_index=True)
    resource_type = models.CharField(
        max_length=100, choices=TYPE_CHOICES, default="Other"
    )
    url = models.URLField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resources")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="Not Started/On Hold"
    )
    description = models.TextField(max_length=455, null=True, blank=True)

    class Meta:
        ordering = ("updated",)

    def __str__(self):
        return self.title


class Subject(models.Model):
    name = models.CharField(max_length=75,
                            unique=True)
    users = models.ManyToManyField(User,
                                   related_name='subjects')

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICE = [("completed", "Completed"), ("todo", "Todo")]
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=150)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="todo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.title


class Note(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="notes"
    )
    title = models.CharField(max_length=250)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title


class Goal(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='goals')
    title = models.CharField(max_length=250)
    subject = models.CharField(max_length=100)
    resources = models.ManyToManyField(Resource,
                                       related_name='goals')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='posts')
    title = models.CharField(max_length=250)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f'Comment by {self.user.username}'


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='replies')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f'Comment reply by {self.user.username}'


class LearningLog(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='logs')
    text = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.text


class Feedback(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='feedback')
    feedback = models.TextField()
    resolved = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return  f"{'[RESOLVED] ' if self.resolved else ''}{self.user.username}'s feedback"
