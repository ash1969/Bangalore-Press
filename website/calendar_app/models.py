from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from django.urls import reverse
# Create your models here.

def content_file_name(instance,filename):
	ext = "png" #Convert every extension into high quality PNG format
	filename = str(instance.name) + "." + str(ext) #Giving the image the name of its festival
	return os.path.join('images/',filename)

class Festivals(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateField()
    religion_choices = (
        ('1', 'Hindu'),
        ('2', 'Muslim'),
        ('3', 'Sikh'),
        ('4', 'Christian'),
        ('5', 'Common'),
    )
    religion = models.CharField(max_length=50, choices=religion_choices, default='5')
    ritu = models.CharField(max_length=30) #Can be given choices as in the case of religion
    masa = models.CharField(max_length=30) #Can be given choices as in the case of religion
    paksha = models.CharField(max_length=30) #Can be given choices as in the case of
    tithi_name = models.CharField(max_length=30) #Can be given choices as in the case of religion
    tithi = models.TimeField()
    nakshtra_name = models.CharField(max_length=30) #Can be given choices as in the case of religion
    nakshtra = models.TimeField()
    sowra = models.IntegerField()
    muhammadan = models.IntegerField()
    rahukala_start = models.TimeField()
    rahukala_end = models.TimeField()
    image = models.ImageField(upload_to=content_file_name)
    description = models.TextField()
    # TODO
    # AUTOGENERATE DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def get_cname(self):  #Can be used to get the class name of the model
        class_name = "Festival"
        return class_name

    class Meta:
        managed = True
        ordering = ['-created_at'] #Will be arranged in order of 'created_at' attribute
        db_table = 'festivals'
        verbose_name_plural = 'Festivals'

    def clean(self):  #Validating the 'rahukala_end' with respect to 'rahukala_start'
        if self.rahukala_end <= self.rahukala_start:
            raise ValidationError('Rahukala Ending Time must after Starting Time!')

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'