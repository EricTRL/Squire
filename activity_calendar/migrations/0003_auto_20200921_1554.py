# Generated by Django 2.2.8 on 2020-09-21 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity_calendar', '0002_auto_20200830_1534'),
    ]

    operations = [
        # This was previously set to parent_activity. But I doubt the person who set this understood its meaning
        # related name is to trace back from the other object back to this. I.e. from the Activity object. To get
        # all activity slots object from the activity object one had to do  activity_obj.parent_activity.all
        # Which does not make sense in this order as the slots are not the parent acitivities. It is therefor set to
        # activity_slot_set which is quite close to the Django default.
        migrations.AlterField(
            model_name='activityslot',
            name='parent_activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_slot_set', to='activity_calendar.Activity'),
        ),
    ]
