# Generated by Django 4.2.4 on 2024-01-11 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0013_remove_activity_log_data_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity_log',
            name='type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
