# Generated by Django 2.2.3 on 2019-12-19 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic_marathon_app', '0008_auto_20191212_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(max_length=400),
        ),
    ]