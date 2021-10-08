# Generated by Django 3.2.7 on 2021-10-01 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telegram', '0005_alter_userprofile_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('date_send', models.DateTimeField(auto_now_add=True, null=True)),
                ('group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='telegram.telegroup')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]