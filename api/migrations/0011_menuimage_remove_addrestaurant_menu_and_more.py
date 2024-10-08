# Generated by Django 5.0.6 on 2024-07-26 12:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_addrestaurant_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='RequestedMenus/')),
            ],
        ),
        migrations.RemoveField(
            model_name='addrestaurant',
            name='menu',
        ),
        migrations.AddField(
            model_name='addrestaurant',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addrestaurant',
            name='menu_images',
            field=models.ManyToManyField(blank=True, related_name='restaurants', to='api.menuimage'),
        ),
    ]
