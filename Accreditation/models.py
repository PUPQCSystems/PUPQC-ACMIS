import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from Programs.models import Programs
from django.contrib.postgres.fields import ArrayField


from Users.models import CustomUser
from . import models_views

 # Create your models here.
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

    def __str__(self):
        return(self.name)


class instrument_level(models.Model):
    instrument = models.ForeignKey(instrument, on_delete=models.CASCADE, related_name='instrument_instrument_level')
    level = models.ForeignKey(accredlevel, on_delete=models.CASCADE, related_name='level_instrument_level')
    description = models.TextField(null=True, blank=True)
    progress_percentage  = models.DecimalField(max_digits=5 ,decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_instrument_level', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_instrument_level', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('instrument', 'level')

    def __str__(self):
            return f"{self.level.name} - {self.instrument.name}"

class instrument_level_folder(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    label = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    instrument_level = models.ForeignKey(instrument_level, on_delete=models.CASCADE, null=True, blank=True)
    parent_directory = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children_directory', null=True, blank=True)
    due_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    progress_percentage  = models.DecimalField(max_digits=5 ,decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_instrument_level_directory', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_instrument_level_directory', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'parent_directory', 'instrument_level')

    
class submission_bin(models.Model):
    parent_directory = models.ForeignKey(instrument_level_folder, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=5000, null=True, blank=True)
    accepted_file_type = models.CharField(max_length=1000, null=True ,blank=True)
    accepted_file_size = models.PositiveSmallIntegerField(blank=True, null=True)
    accepted_file_count = models.PositiveSmallIntegerField(blank=True, null=True)
    status  = models.CharField(max_length=50, null=True, blank=True)
    remarks =  models.CharField(max_length=2000, null=True, blank=True)
    reviewed_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='reviewed_submission_bin', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_submission_bin', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_submission_bin', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return(self.title)
    

class files(models.Model):
    upload_bin = models.ForeignKey(submission_bin, on_delete=models.CASCADE, null=True, blank=True)
    parent_directory = models.ForeignKey(instrument_level_folder, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to = 'uploaded-files/')
    file_name = models.CharField(max_length=100, null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_upload_files', null=True, blank=True)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_upload_files', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.file_name)