from django.contrib import admin

from .models import Note, Resource, Task, Goal, Post, Subject, Comment, Feedback


admin.site.register(Resource)
admin.site.register(Note)
admin.site.register(Subject)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Feedback)
