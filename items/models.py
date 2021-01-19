from django.db import models
from django.conf.global_settings import MEDIA_ROOT

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="photos", max_length=100)
    weight = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=20)