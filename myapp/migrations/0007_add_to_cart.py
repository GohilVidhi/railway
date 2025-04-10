# Generated by Django 5.1.4 on 2025-02-27 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_product_sub_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_to_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=25, null=True)),
                ('price', models.IntegerField(default=0)),
                ('totalprice', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.product')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
