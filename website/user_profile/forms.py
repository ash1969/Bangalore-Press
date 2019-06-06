from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField

class Profileform(forms.ModelForm):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    mobile = PhoneNumberField()
    referral_used = models.CharField(max_length=10)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'religion', 'date_of_birth', 'mobile', 'referral_used',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Mandatory')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )