# Generated by Django 4.2.4 on 2024-01-13 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0018_alter_parameter_components_modified_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter_components',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
