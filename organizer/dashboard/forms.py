from django import forms

from .models import Resource


class AddResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ("title", "subject", "resource_type",
                  "url")
