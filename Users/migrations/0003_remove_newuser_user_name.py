# Generated by Django 4.2.4 on 2023-10-05 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_newuser_last_name_newuser_middle_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_name',
        ),
    ]
