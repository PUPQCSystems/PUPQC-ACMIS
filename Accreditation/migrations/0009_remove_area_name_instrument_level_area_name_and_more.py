# Generated by Django 4.2.4 on 2023-12-16 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0008_alter_instrument_accredbodies_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='name',
        ),
        migrations.AddField(
            model_name='instrument_level_area',
            name='name',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='instrument_level_area',
            unique_together={('area', 'instrument_level')},
        ),
    ]
