# Generated by Django 5.0.1 on 2024-04-28 05:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0087_alter_instrument_level_folder_instrument_level_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='files',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='files',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='related_reviewer_files', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='files',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]