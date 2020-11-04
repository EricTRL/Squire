# Generated by Django 2.2.3 on 2020-11-04 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_calendar', '0005_activitymoment_local_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityslot',
            name='location_is_private',
            field=models.BooleanField(default=False, help_text='Private locations are hidden for users not registered to this slot', verbose_name='private location?'),
        ),
    ]