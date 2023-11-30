# Generated by Django 4.2.4 on 2023-11-24 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accreditation', '0004_accredbodies'),
    ]

    operations = [
        migrations.AddField(
            model_name='accredbodies',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_bodies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accredbodies',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accredbodies',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_bodies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accredlevel',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_levels', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accredlevel',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accredlevel',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_levels', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accredtype',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_type', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accredtype',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accredtype',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_type', to=settings.AUTH_USER_MODEL),
        ),
    ]