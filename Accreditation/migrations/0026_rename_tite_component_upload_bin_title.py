# Generated by Django 4.2.4 on 2024-01-20 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0025_component_upload_bin_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='component_upload_bin',
            old_name='tite',
            new_name='title',
        ),
    ]
