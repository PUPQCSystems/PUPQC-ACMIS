# Generated by Django 5.0.1 on 2024-02-29 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0067_program_accreditation_entry_result_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program_accreditation',
            old_name='entry_result_date',
            new_name='entry_result_at',
        ),
    ]
