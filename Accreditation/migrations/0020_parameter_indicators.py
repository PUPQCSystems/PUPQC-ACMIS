# Generated by Django 4.2.4 on 2024-01-14 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accreditation', '0019_alter_parameter_components_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='parameter_indicators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('area_parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accreditation.level_area_parameter')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accreditation.parameter_components')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_parameter_indicators', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_parameter_indicators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]