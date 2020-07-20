from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Not Started/On Hold', "Not Started/On Hold")
    )
    TYPE_CHOICES = (
        ('Video Course', "Video Course"),
        ('Text Course', 'Text Course'),
        ('Text Tutorial', 'Text Tutorial'),
        ('Video Tutorial', 'Video Tutorial'),
        ('eBook', 'eBook'),
        ('Book', 'Book'),
        ('Other', 'Other'),
    )
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=100,
                                     choices=TYPE_CHOICES,
                                     default='other')
    url = models.URLField(max_length=255,
                                   null=True)
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
