# Generated by Django 3.2.7 on 2021-09-29 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0004_alter_userprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default='Не вказано', max_length=120, null=True),
        ),
    ]
