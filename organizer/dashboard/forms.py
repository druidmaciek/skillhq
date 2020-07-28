from django import forms

from .models import Resource, Post, Comment, CommentReply


class AddResourceForm(forms.ModelForm):

    url = forms.URLField(required=False)

    class Meta:
        model = Resource
        fields = ("title", "subject", "resource_type", "url", "description")


class AddDiscussionForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content")


class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)


class AddCommentReplyForm(forms.ModelForm):

    class Meta:
        model = CommentReply
        fields = ('content',)


