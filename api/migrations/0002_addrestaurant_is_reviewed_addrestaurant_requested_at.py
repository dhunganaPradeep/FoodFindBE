from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
         ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='addrestaurant',
            name='is_reviewed',
            field=models.BooleanField(default=False),
        ), 
        migrations.AddField(
            model_name='addrestaurant',
            name='requested_at',
            field=models.DateTimeField(default=datetime.datetime.now),  # Use an appropriate default
        ),
    ]
