# Generated by Django 4.2.4 on 2023-11-27 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_rename_id_customuser_profile_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser_profile',
            old_name='street_addres',
            new_name='street_address',
        ),
    ]