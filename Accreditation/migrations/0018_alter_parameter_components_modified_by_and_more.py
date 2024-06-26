# Generated by Django 4.2.4 on 2024-01-13 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accreditation', '0017_parameter_components'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter_components',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_parameter_components', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='parameter_components',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
