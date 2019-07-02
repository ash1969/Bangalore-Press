from django import forms
from .models import *

class Locationform(forms.Form):
    Enter_your_location = forms.CharField(max_length=100)