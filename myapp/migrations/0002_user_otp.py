# Generated by Django 5.1.4 on 2025-02-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]
