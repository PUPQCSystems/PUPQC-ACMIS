from django.db import models
from django.conf import settings
from django.utils import timezone

 # Create your models here.

class Programs(models.Model):
    program_name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10)
    description = models.TextField()
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_programs')
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_programs', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return '%s %s' % (self.program_name, '(' + self.abbreviation + ')')