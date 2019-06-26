from django import forms
from .models import *

class Locationform(forms.Form):
    location = forms.CharField(max_length=100)