# Generated by Django 2.0.2 on 2018-04-23 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_traitvaluedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='traitvaluedetails',
            name='recommendations_negative_feedbacks',
            field=models.CharField(default='abc', max_length=100),
        ),
        migrations.AddField(
            model_name='traitvaluedetails',
            name='recommendations_positive_feedbacks',
            field=models.CharField(default='abc', max_length=100),
        ),
    ]