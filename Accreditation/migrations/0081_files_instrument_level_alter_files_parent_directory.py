# Generated by Django 5.0.1 on 2024-03-28 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0080_remove_files_size_in_mb'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='instrument_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Accreditation.instrument_level'),
        ),
        migrations.AlterField(
            model_name='files',
            name='parent_directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Accreditation.instrument_level_folder'),
        ),
    ]