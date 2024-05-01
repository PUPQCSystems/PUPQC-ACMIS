import os
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from Programs.models import Programs
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import default_storage # Import for renaming the file


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
    description = models.TextField(null=True, blank=True)
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
    description = models.TextField(null=True, blank=True)
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
    name = models.CharField(max_length=250, null=False, blank=False)
    label = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    instrument_level = models.ForeignKey(instrument_level, related_name='instrument_level_folder_relation', on_delete=models.CASCADE, null=True, blank=True)
    parent_directory = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children_directory', null=True, blank=True)
    due_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    progress_percentage  = models.DecimalField(max_digits=5 ,decimal_places=2, null=True, blank=True)
    has_progress_bar = models.BooleanField(default=False)
    has_assign_button = models.BooleanField(default=False)
    is_advance = models.BooleanField(default=False)
    is_submission_bin = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    can_be_reviewed = models.BooleanField(default=False)
    accepted_file_type = models.CharField(max_length=1000, null=True ,blank=True)
    accepted_file_size = models.PositiveSmallIntegerField(blank=True, null=True)
    accepted_file_count = models.PositiveSmallIntegerField(blank=True, null=True)
    status  = models.CharField(max_length=50, null=True, blank=True)
    remarks =  models.TextField(null=True, blank=True)
    reviewed_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='reviewed_submission_bin', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_instrument_level_directory', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_instrument_level_directory', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'parent_directory', 'instrument_level')


    def __str__(self):
        return(self.title)
    

class files(models.Model):
    instrument_level = models.ForeignKey(instrument_level, on_delete=models.CASCADE, null=True, blank=True) 
    parent_directory = models.ForeignKey(instrument_level_folder, on_delete=models.CASCADE, null=True, blank=True)
    file_path = models.FileField(upload_to = 'uploaded-files/')
    file_name = models.CharField(max_length=300, null=True, blank=True)
    can_be_reviewed = models.BooleanField(default=True)
    status  = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    reviewed_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='related_reviewer_files', null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_upload_files', null=True, blank=True)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_upload_files', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.file_name)
    
    def delete(self,*args, **kwargs):
        self.file_path.delete()
        super().delete(*args, **kwargs)

    def rename_save(self, *args, **kwargs):
        new_file_name = self.file_name  
        old_file_path = self.file_path.name

        # Rename with extension preservation:
        if self.pk and old_file_path and new_file_name != os.path.basename(old_file_path):
            old_directory, old_base = os.path.split(old_file_path) # Split into dir and file
            old_extension = os.path.splitext(old_base)[1]

            # Only add extension if the new name doesn't have one
            if not os.path.splitext(new_file_name)[1]:
                new_file_name += old_extension

            new_file_path = os.path.join(old_directory, new_file_name) # Use the original directory

            try:
                default_storage.save(new_file_path, default_storage.open(old_file_path))
                self.file_path = new_file_path
                default_storage.delete(old_file_path)
            except:  
                pass  # Handle potential errors gracefully

        super().save(*args, **kwargs)



class program_accreditation(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, null=True, blank=True, related_name='program_relation')
    instrument_level = models.ForeignKey(instrument_level, on_delete=models.CASCADE, null=True, blank=True, related_name='instrument_level_relation')
    description = models.CharField(max_length=5000, null=True, blank=True)
    mock_accred_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    survey_visit_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    revisit_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False)
    status = models.CharField(max_length=50, null=True, blank=True)
    entry_result_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    validity_date_from = models.DateTimeField(auto_now=False, null=True, blank=True)
    validity_date_to = models.DateTimeField(auto_now=False, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_program_accreditation', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_program_accreditation', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('program', 'instrument_level')


class result_remarks(models.Model):
    accredited_program = models.ForeignKey(program_accreditation, on_delete=models.CASCADE, null=True, blank=True, related_name='program_remarks_relation')
    remarks = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_result_remarks', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_result_remarks', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)


class accreditation_certificates(models.Model):
    accredited_program = models.ForeignKey(program_accreditation, related_name='accredited_program_certificate', on_delete=models.CASCADE, null=True, blank=True)
    certificate_path = models.FileField(upload_to = 'accreditation-certifacates/', max_length=300)
    certificate_name = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_accreditation_certificate', null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_accreditation_certificate', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return(self.accredited_program.program)
    
    def delete(self,*args, **kwargs):
        self.certificate_path.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        new_file_name = self.file_name  
        old_file_path = self.file_path.name

        # Rename with extension preservation:
        if self.pk and old_file_path and new_file_name != os.path.basename(old_file_path):
            old_directory, old_base = os.path.split(old_file_path) # Split into dir and file
            old_extension = os.path.splitext(old_base)[1]

            # Only add extension if the new name doesn't have one
            if not os.path.splitext(new_file_name)[1]:
                new_file_name += old_extension

            new_file_path = os.path.join(old_directory, new_file_name) # Use the original directory

            try:
                default_storage.save(new_file_path, default_storage.open(old_file_path))
                self.file_path = new_file_path
                default_storage.delete(old_file_path)
            except:  
                pass  # Handle potential errors gracefully

        super().save(*args, **kwargs)

    
class user_assigned_to_folder(models.Model):
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='assigned_user', null=False, blank=False)
    parent_directory = models.ForeignKey(instrument_level_folder, related_name='assigned_parent_folder', on_delete=models.CASCADE, null=False, blank=False)
    is_chairman = models.BooleanField(default=False,  null=True, blank=True)
    is_cochairman = models.BooleanField(default=False,  null=True, blank=True)
    is_member = models.BooleanField(default=False,  null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assigned_by', null=True, blank=True)
    assigned_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_by_assignees', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    removed_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('assigned_user', 'parent_directory')