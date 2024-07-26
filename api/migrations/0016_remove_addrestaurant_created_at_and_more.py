# Generated by Django 5.0.6 on 2024-07-26 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_menuimage_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addrestaurant',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='menuimage',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='addrestaurant',
            name='menu_images',
            field=models.ManyToManyField(blank=True, related_name='restaurants', to='api.menuimage'),
        ),
    ]