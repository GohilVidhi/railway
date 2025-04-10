# Generated by Django 5.1.4 on 2025-03-26 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_check_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('resident_address', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=20)),
                ('pincode', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Check',
        ),
    ]
