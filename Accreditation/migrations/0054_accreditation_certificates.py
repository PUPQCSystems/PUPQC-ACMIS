# Generated by Django 5.0.1 on 2024-02-10 09:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0053_program_accreditation_mock_accred_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='accreditation_certificates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_path', models.FileField(upload_to='accreditation-certifacates/')),
                ('certificate_name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('accredited_program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accredited_program_certificate', to='Accreditation.program_accreditation')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_accreditation_certificate', to=settings.AUTH_USER_MODEL)),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_accreditation_certificate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]