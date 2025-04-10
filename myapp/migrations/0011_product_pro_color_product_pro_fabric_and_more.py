# Generated by Django 5.1.4 on 2025-03-18 08:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_color_fabric_price_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pro_Color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='pro_fabric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.fabric'),
        ),
        migrations.AddField(
            model_name='product',
            name='pro_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.price'),
        ),
        migrations.AddField(
            model_name='product',
            name='pro_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.size'),
        ),
    ]
