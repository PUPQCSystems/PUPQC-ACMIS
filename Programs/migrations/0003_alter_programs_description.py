# Generated by Django 4.2.4 on 2024-01-07 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Programs', '0002_alter_programs_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programs',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
