from django import forms

from .models import Author, NewsStory

class PostForm(forms.ModelForm):

    class Meta:
        model = NewsStory
        fields = ('headline', 'category', 'region', 'details')