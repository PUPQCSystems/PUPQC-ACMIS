# Generated by Django 5.0.1 on 2024-03-24 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0076_instrument_level_folder_has_assign_button_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument_level_folder',
            name='name',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]