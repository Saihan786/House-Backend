from django.db import models

class Region(models.Model):
    outer_polygon = models.FileField()