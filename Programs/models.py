from django.db import models
from django.utils import timezone

 # Create your models here.

 
class Programs(models.Model):
    program_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    description = models.TextField()
    # created_by = models.ForeignKey()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    color_code = models.CharField(max_length=7)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


    