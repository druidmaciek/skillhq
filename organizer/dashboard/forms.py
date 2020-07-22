from django import forms

from .models import Resource


class AddResourceForm(forms.ModelForm):

    url = forms.URLField(required=False)

    class Meta:
        model = Resource
        fields = ("title", "subject", "resource_type",
                  "url", 'description')
