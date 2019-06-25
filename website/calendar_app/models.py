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
    religion_choices = (
        ('1', 'Hindu'),
        ('2', 'Muslim'),
        ('3', 'Sikh'),
        ('4', 'Christian'),
        ('5', 'Jain'),
        ('6', 'Other'),
    )
    religion = models.CharField(max_length=50, choices=religion_choices, default='6')
    samvatsara_choices = (
        ('Prabhava', 'Prabhava'),
        ('Vibhava', 'Vibhava'),
        ('Shukla', 'Shukla'),
        ('Pramodaduta', 'Pramodaduta'),
        ('Prajapati', 'Prajapati'),
        ('Angirasa', 'Angirasa'),
        ('Shrimukha', 'Shrimukha'),
        ('Bhava', 'Bhava'),
        ('Yuva', 'Yuva'),
        ('Dhatru', 'Dhatru'),
        ('Ishwara', 'Ishwara'),
        ('BahuDhaanya', 'BahuDhaanya'),
        ('Pramathi', 'Pramathi'),
        ('Vikrama', 'Vikrama'),
        ('Vrushapraja', 'Vrushapraja'),
        ('Chaitrabhanu', 'Chaitrabhanu'),
        ('Subhanu', 'Subhanu'),
        ('Tarana', 'Tarana'),
        ('Parthiva', 'Parthiva'),
        ('Vyaya', 'Vyaya'),
        ('Sarvajit', 'Sarvajit'),
        ('Sarvadharin', 'Sarvadharin'),
        ('Virodhin', 'Virodhin'),
        ('Vikrti', 'Vikrti'),
        ('Khara', 'Khara'),
        ('Nandana', 'Nandana'),
        ('Vijaya', 'Vijaya'),
        ('Jaya', 'Jaya'),
        ('Manmatha', 'Manmatha'),
        ('Durmukha', 'Durmukha'),
        ('Hevilambi', 'Hevilambi'),
        ('Vilambi', 'Vilambi'),
        ('Vikari', 'Vikari'),
        ('Sarvarin', 'Sarvarin'),
        ('Plava', 'Plava'),
        ('Subhakrta', 'Subhakrta'),
        ('Sobhana', 'Sobhana'),
        ('Krodhin', 'Krodhin'),
        ('Visvavasu', 'Visvavasu'),
        ('Parabhava', 'Parabhava'),
        ('Plavanga', 'Plavanga'),
        ('Kilaka', 'Kilaka'),
        ('Saumya', 'Saumya'),
        ('Sadharana', 'Sadharana'),
        ('Virodhakrta', 'Virodhakrta'),
        ('Paridhavin', 'Paridhavin'),
        ('Pramadin', 'Pramadin'),
        ('Ananda', 'Ananda'),
        ('Raksasa', 'Raksasa'),
        ('Nala/Anala', 'Nala/Anala'),
        ('Pingala', 'Pingala'),
        ('Kalayukta', 'Kalayukta'),
        ('Siddharthin', 'Siddharthin'),
        ('Raudra', 'Raudra'),
        ('Durmati', 'Durmati'),
        ('Dundubhi', 'Dundubhi'),
        ('Rudhirodgarin', 'Rudhirodgarin'),
        ('Raktaksin', 'Raktaksin'),
        ('Krodhana/Manyu', 'Krodhana/Manyu'),
        ('Akshaya', 'Akshaya'),
    )
    samvatsara = models.CharField(max_length=50, choices=samvatsara_choices, blank=True, null=True)
    aayana_choices = (
        ('Dakshinayana', 'Dakshinayana'),
        ('Uttarayana', 'Uttarayana'),
    )
    aayana = models.CharField(max_length=50, choices=aayana_choices, blank=True, null=True)
    rithu_choices = (
        ('Vasantha', 'Vasantha'),
        ('Grishma', 'Grishma'),
        ('Varsha', 'Varsha'),
        ('Sharad', 'Sharad'),
        ('Hemantha', 'Hemantha'),
        ('Shishira', 'Shishira'),
    )
    rithu = models.CharField(max_length=50, choices=rithu_choices, blank=True, null=True)
    maasa_choices = (
        ('Chaitra', 'Chaitra'),
        ('Vaishaka', 'Vaishaka'),
        ('Jyeshta', 'Jyeshta'),
        ('Ashada', 'Ashada'),
        ('Shravana', 'Shravana'),
        ('Bhaadrapada', 'Bhaadrapada'),
        ('Ashwayuja', 'Ashwayuja'),
        ('Kaarthik', 'Kaarthik'),
        ('Margshira', 'Margshira'),
        ('Pushya', 'Pushya'),
        ('Maagha', 'Maagha'),
        ('Phalguna', 'Phalguna'),
    )
    maasa = models.CharField(max_length=50, choices=maasa_choices, blank=True, null=True)
    paksha_choices = (
        ('Krishna', 'Krishna'),
        ('Shukla', 'Shukla'),
    )
    paksha = models.CharField(max_length=50, choices=paksha_choices, blank=True, null=True)
    tithi_choices = (
        ('Pratipat', 'Pratipat'),
        ('Dvitya', 'Dvitya'),
        ('Tritiya', 'Tritiya'),
        ('Chaturthi', 'Chaturthi'),
        ('Panchami', 'Panchami'),
        ('Shashti', 'Shashti'),
        ('Saptami', 'Saptami'),
        ('Ashtami', 'Ashtami'),
        ('Navami', 'Navami'),
        ('Ekadashi', 'Ekadashi'),
        ('Dwadashi', 'Dwadashi'),
        ('Trayodashi', 'Trayodashi'),
        ('Chaturdashi', 'Chaturdashi'),
        ('Poornima', 'Poornima (Shukla)'),
        ('Amavasya', 'Amavasya (Krishna)'),
    )
    tithi = models.CharField(max_length=50, choices=tithi_choices, blank=True, null=True)
    tithi_upto = models.DateTimeField(blank=True, null=True)
    nakshtra_choices = (
        ('Ashwini', 'Ashwini'),
        ('Bharani', 'Bharani'),
        ('Krittika', 'Krittika'),
        ('Rohini', 'Rohini'),
        ('Mrigashira', 'Mrigashira'),
        ('Aridhra', 'Aridhra'),
        ('Punarvasu', 'Punarvasu'),
        ('Pushya', 'Pushya'),
        ('Ashlesha', 'Ashlesha'),
        ('Magha', 'Magha'),
        ('Poorva Phalguni', 'Poorva Phalguni'),
        ('Uttara', 'Uttara'),
        ('Hastaa', 'Hastaa'),
        ('Chitra', 'Chitra'),
        ('Swathi', 'Swathi'),
        ('Vishaka', 'Vishaka'),
        ('Anuradha', 'Anuradha'),
        ('Jyeshta', 'Jyeshta'),
        ('Moola', 'Moola'),
        ('Pooravashada', 'Pooravashada'),
        ('Uttarashada', 'Uttarashada'),
        ('Shravana', 'Shravana'),
        ('Dhanishta', 'Dhanishta'),
        ('Shatabhisha', 'Shatabhisha'),
        ('Poorva Bhadrapada', 'Poorva Bhadrapada'),
        ('Uttara Bhadrapada', 'Uttara Bhadrapada'),
        ('Revathi', 'Revathi'),
    )
    nakshtra = models.CharField(max_length=50, choices=nakshtra_choices, blank=True, null=True)
    nakshtra_upto = models.DateTimeField(blank=True, null=True)
    sowra = models.IntegerField(blank=True, null=True)
    muhammadan = models.IntegerField(blank=True, null=True)
    rahukaala_start = models.TimeField(blank=True, null=True)
    rahukaala_end = models.TimeField(blank=True, null=True)
    gulikaala_start = models.TimeField(blank=True, null=True)
    gulikaala_end = models.TimeField(blank=True, null=True)
    yamaganda_kaala_start = models.TimeField(blank=True, null=True)
    yamaganda_kaala_end = models.TimeField(blank=True, null=True)
    date = models.DateTimeField()
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

    def clean(self):
         if self.rahukaala_start != None:
            if self.rahukaala_end <= self.rahukaala_start:
              raise ValidationError('Rahukaala Ending Time must after Starting Time!')

    def clean(self):
        if self.gulikaala_start != None:
          if self.gulikaala_end <= self.gulikaala_start:
            raise ValidationError('Gulikaala Ending Time must after Starting Time!')

    def clean(self):
        if self.yamaganda_kaala_start != None:
          if self.yamaganda_kaala_end <= self.yamaganda_kaala_start:
            raise ValidationError('Yamaganda Kaala Ending Time must after Starting Time!')

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'