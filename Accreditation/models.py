import uuid
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
    

class area(models.Model):
    area_number = models.CharField(max_length=15, unique=True)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_areas', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_areas', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.area_number)
    
class parameter(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_parameters', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_parameters', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.name)

    
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

    class Meta:
        unique_together = ('accredbodies', 'program')


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

    class Meta:
        unique_together = ('instrument', 'level')

class instrument_level_area(models.Model):
    area = models.ForeignKey(area, on_delete=models.CASCADE)
    label = models.CharField(max_length=250, null=True, blank=True)
    instrument_level = models.ForeignKey(instrument_level, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_instrument_level_area', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_instrument_level_area', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('area', 'instrument_level')


class level_area_parameter(models.Model):
    parameter = models.ForeignKey(parameter, on_delete=models.CASCADE)
    label = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    instrument_level_area = models.ForeignKey(instrument_level_area, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_level_area_parameter', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_level_area_parameter', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('parameter', 'instrument_level_area')

class components(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_components', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_components', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.name)
    
class parameter_components(models.Model):
    component = models.ForeignKey(components, on_delete=models.CASCADE, null=True, blank=True)
    area_parameter = models.ForeignKey(level_area_parameter, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_parameter_components', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_parameter_components', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('component', 'area_parameter')

    #I add this code so that the parameter_components object can accept additional field. This code fixes the error
    # parameter_components() got unexpected keyword arguments: 'component_update_form'
    def __init__(self, *args, **kwargs):
        component_update_form = kwargs.pop('component_update_form', None)
        super(parameter_components, self).__init__(*args, **kwargs)
        self.component_update_form = component_update_form
    
class component_upload_bin(models.Model):
    tite = models.CharField(max_length=2000, null=True, blank=True, unique=True)
    description
    parameter_component = models.ForeignKey(parameter_components, on_delete=models.CASCADE)
    sub_indicator = models.ForeignKey('self', null=True, blank=True ,on_delete=models.CASCADE, related_name='sub_indicators',)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_parameter_indicators', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_parameter_indicators', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.number, '. ' + self.name)
    



