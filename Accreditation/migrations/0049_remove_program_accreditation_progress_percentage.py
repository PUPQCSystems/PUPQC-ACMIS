# Generated by Django 5.0.1 on 2024-02-04 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0048_remove_program_accreditation_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program_accreditation',
            name='progress_percentage',
        ),
    ]
