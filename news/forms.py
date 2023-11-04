from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_name',
            'post_text',
            'post_category'
            ]