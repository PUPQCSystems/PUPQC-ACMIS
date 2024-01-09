from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, middle_name , last_name ,password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, middle_name , last_name ,password, **other_fields)

    def create_user(self, email, first_name, middle_name , last_name ,password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name, middle_name=middle_name , last_name=last_name,**other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    profile_pic = models.TextField(blank=True)
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_customuser', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_customuser', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    deactivated_at = models.DateTimeField(auto_now=False, null=True, blank=True)


    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name']

    def __str__(self):
        return self.first_name
    
class CustomUser_profile(models.Model):
    account = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    birth_date = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=150, blank=True, null=True)
    sex = models.CharField(max_length=6,blank=True, null=True)
    civil_status = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=20, blank=True, null=True)
    personal_no = models.CharField(max_length=11, blank=True, null=True)
    contact_no = models.CharField(max_length=11, blank=True, null=True)
    contact_email = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    house_no = models.CharField(max_length=30, blank=True, null=True)
    street_address = models.CharField(max_length=30, blank=True, null=True)
    barangay = models.CharField(max_length=30, blank=True, null=True)
    modified_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_profile', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

class activity_log(models.Model):
    acted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='acted_by', null=True, blank=True)
    module = models.CharField(max_length=250, null=True, blank=True)
    action = models.CharField(max_length=250, null=True, blank=True)
    data_entry = models.CharField(max_length=250, null=True, blank=True)
    datetime_acted = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


