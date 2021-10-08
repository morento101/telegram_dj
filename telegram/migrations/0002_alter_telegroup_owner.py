# Generated by Django 3.2.7 on 2021-09-28 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegroup',
            name='owner',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
