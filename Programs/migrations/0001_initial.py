# Generated by Django 4.2.4 on 2023-09-04 15:37

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=100, unique=True)),
                ('abbreviation', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_programs', null=True, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified_programs', null=True, blank=True)),
                ('deleted_at', models.DateTimeField(auto_now=False, null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
  
            ],
        ),
    ]
