from django.contrib import admin

from .models import Note, Resource

admin.site.register(Resource)
admin.site.register(Note)
