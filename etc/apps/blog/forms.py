from django import forms
from .models import Comments, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags',
                  'city', 'img']


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text_comments',)
