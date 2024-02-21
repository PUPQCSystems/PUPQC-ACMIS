# Generated by Django 5.0.1 on 2024-02-21 08:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0058_alter_user_assigned_to_area_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user_assigned_to_area',
            unique_together={('assigned_user', 'area')},
        ),
    ]
