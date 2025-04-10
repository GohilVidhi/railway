# Generated by Django 4.2 on 2025-03-26 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_address_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('sub_total', models.IntegerField()),
                ('shipping', models.CharField(max_length=100)),
                ('coupon', models.IntegerField()),
                ('total', models.IntegerField()),
                ('address_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.address')),
                ('cart_data', models.ManyToManyField(blank=True, null=True, to='myapp.add_to_cart')),
                ('user_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
