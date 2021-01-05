from django.db import models

# Create your models here.
class ImageDetails(models.Model):
    img_name = models.CharField(max_length=100, blank=True, null=True)
    img = models.ImageField(upload_to='media/', blank=True, null=True)
    
class TestUploadImage(models.Model):
    testimg = models.ImageField(upload_to='testmedia/', blank=True, null=True)
