from django.db import models

# Create your models here
class Photographer(models.Model):
    external_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=250)

class Photo(models.Model):

    # FK
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)

    external_id = models.BigIntegerField(unique=True)
    width = models.IntegerField()
    height = models.IntegerField()
    url = models.CharField(max_length=250, unique=True)
    avg_color = models.CharField(max_length=32)
    alt = models.CharField(max_length=250)

class PhotoVariant(models.Model):
    class VARIANTS_NAMES(models.TextChoices):
        ORIGINAL = ("original")
        LARGE2X = ("large2x")
        LARGE = ("large")
        MEDIUM = ("medium")
        SMALL = ("small")
        PORTRAIT = ("portrait")
        LANDSCAPE = ("landscape")
        TINY = ("tiny")

    original_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=100)
    url = models.CharField(max_length=250, unique=True)
