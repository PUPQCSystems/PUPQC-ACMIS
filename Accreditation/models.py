from django.db import models
from django.utils import timezone

 # Create your models here.

 
# class type(models.Model):
#     name = models.CharField(max_length=20, unique=True)
#     description = models.CharField(max_length=2000)
#     # created_by = models.ForeignKey()
#     created_at = models.DateTimeField(default=timezone.now)
#     modified_at = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)

class accredtype(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=2000)
    # created_by = models.ForeignKey()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
