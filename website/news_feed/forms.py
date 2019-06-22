from django import forms
from .models import *
from django.contrib.auth.models import User

class Postform(forms.ModelForm):
    caption = models.CharField(max_length=100)

    class Meta:
        model = Post
        fields = ('caption', 'image', 'category',)
