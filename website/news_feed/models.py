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

def content_file_name(instance,filename):
	ext = "png" #Convert every extension into high quality PNG format
	filename = str(instance.caption) + "." + str(ext) #Giving the image the name of its festival
	return os.path.join('images/',filename)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to=content_file_name)
    category_choices = (
        ('1', 'Literature'),
        ('2', 'History'),
        ('3', 'Monuments'),
        ('4', 'Arts'),
        ('5', 'Customs'),
        ('6', 'Rituals'),
        ('7', 'Culture')
    )
    category = models.CharField(max_length=50, choices=category_choices, default='7')
    # TODO
    # AUTOGENERATE DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.caption

    def get_cname(self):
        cat = self.category
        if cat=='1':
            cname = "Literature"
        elif cat=='2':
            cname = "History"
        elif cat=='3':
            cname = "Monuments"
        elif cat=='4':
            cname = "Arts"
        elif cat=='5':
            cname = "Customs"
        elif cat=='6':
            cname = "Rituals"
        else:
            cname = "Culture"
        return cname

    def like_count(self):
        count = Upvotes.objects.filter(post=self)
        return count.count()

    class Meta:
        managed = True

class Upvotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # TBD
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __self__(self):
        return self.post
    class Meta:
        managed = True
        db_table = 'upvotes'
        verbose_name_plural = 'Upvotes'