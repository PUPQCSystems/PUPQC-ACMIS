# Generated by Django 4.2.4 on 2024-01-09 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0015_level_area_parameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='level_area_parameter',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
