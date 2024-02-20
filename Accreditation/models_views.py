import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from Programs.models import Programs
from django.contrib.postgres.fields import ArrayField


class UserGroupView(models.Model):   
    id = models.BigIntegerField(primary_key=True)
    email = models.CharField(max_length=254)
    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    profile_pic = models.CharField(max_length=100)
    user_group = models.CharField(max_length=150)

    class Meta:
            managed = False
            db_table='user_group_view'