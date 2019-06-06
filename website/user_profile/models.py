# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    religion_choices = (
        ('1', 'Hindu'),
        ('2', 'Muslim'),
        ('3', 'Sikh'),
        ('4', 'Christian'),
        ('5', 'Not Interested')
    )
    religion = models.CharField(max_length=50, choices=religion_choices, default='5')
    date_of_birth = models.DateField(blank=True, null=True)
    mobile = PhoneNumberField(blank=True, null=True)
    referral_code = models.CharField(max_length=10)
    referral_used = models.CharField(max_length=10, blank=True, null=True)
    role_choices = (
        ('1', 'Superuser'),
        ('2', 'Moderator'),
        ('3', 'User')
    )
    role = models.CharField(max_length=50, choices=role_choices ,default='3')
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        managed = True

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
