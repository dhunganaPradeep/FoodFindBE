# Generated by Django 5.0.4 on 2024-06-09 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FoodFind', '0006_tag_restaurant_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='review',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='toprestaurant',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='restaurantimage',
            name='restaurant',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='TopRestaurant',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.DeleteModel(
            name='RestaurantImage',
        ),
    ]
