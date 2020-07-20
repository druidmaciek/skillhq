from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('paused', "Not Started/On Hold")
    )
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    resource_url = models.URLField(max_length=255,
                                   null=True,
                                   default=None)
    user = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='resources')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30,
                              choices=STATUS_CHOICES,
                              default='paused')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Note(models.Model):
    resource = models.ForeignKey(Resource,
                                 on_delete=models.CASCADE,
                                 related_name='notes')
    content = models.TextField()