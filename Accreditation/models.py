from django.db import models
from django.conf import settings
from django.utils import timezone
from Programs.models import Programs

 # Create your models here.

class accredtype(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=2000)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_type', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_type', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

class accredlevel(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=2000)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_levels', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_levels', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.name)
    
class accredbodies(models.Model):
    name = models.CharField(max_length=250, unique=True)
    abbreviation = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_bodies', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_bodies', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.name, '(' + self.abbreviation + ')')

    

class instrument(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    accredbodies = models.ForeignKey(accredbodies, on_delete=models.CASCADE, related_name='accredbodies_instrument')
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='programs_instrument')
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_instrument', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_instrument', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class instrument_level(models.Model):
    instrument = models.ForeignKey(instrument, on_delete=models.CASCADE, related_name='instrument_instrument_level')
    level = models.ForeignKey(accredlevel, on_delete=models.CASCADE, related_name='level_instrument_level')
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_instrument_level', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_instrument_level', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

class area(models.Model):
    area_number = models.CharField(max_length=15)
    name = models.CharField(max_length=250, unique=True)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_areas', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_areas', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

class instrument_level_area(models.Model):
    area = models.ForeignKey(area, on_delete=models.CASCADE)
    instrument_level = models.ForeignKey(instrument_level, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_instrument_level_area', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_instrument_level_area', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
