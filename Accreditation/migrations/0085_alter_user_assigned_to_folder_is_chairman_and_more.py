# Generated by Django 5.0.1 on 2024-03-30 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0084_instrument_level_folder_can_be_reviewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_assigned_to_folder',
            name='is_chairman',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user_assigned_to_folder',
            name='is_cochairman',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user_assigned_to_folder',
            name='is_member',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]