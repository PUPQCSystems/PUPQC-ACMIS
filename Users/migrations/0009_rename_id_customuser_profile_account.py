# Generated by Django 4.2.4 on 2023-11-27 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_customuser_profile_modified_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser_profile',
            old_name='id',
            new_name='account',
        ),
    ]