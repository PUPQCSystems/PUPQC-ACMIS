from django.db import models
from django.utils import timezone

 # Create your models here.

class accredtype(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=2000)
    # created_by = models.ForeignKey()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

class accredlevel(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=2000)
    # created_by = models.ForeignKey()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

class accredbodies(models.Model):
    name = models.CharField(max_length=250, unique=True)
    abbreviation = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    # created_by = models.ForeignKey()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)