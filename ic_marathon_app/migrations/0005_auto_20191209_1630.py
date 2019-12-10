# Generated by Django 2.2.3 on 2019-12-09 16:30

from django.db import migrations, models
import ic_marathon_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0004_workout_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='date_time',
            field=models.DateTimeField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='time',
            field=models.TimeField(default='00:00', help_text='Workout in minutes', validators=[ic_marathon_app.validators.validate_workout_time], verbose_name='Duration'),
        ),
    ]