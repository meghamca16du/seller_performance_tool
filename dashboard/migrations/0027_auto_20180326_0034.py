# Generated by Django 2.0.2 on 2018-03-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_traitvaluedetails_recommendations_lateshipmentrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='traitvaluedetails',
            name='recommendations_HitToSucessRatio',
            field=models.TextField(default='abc', max_length=100),
        ),
        migrations.AddField(
            model_name='traitvaluedetails',
            name='recommendations_onTimeDeliery',
            field=models.TextField(default='abc', max_length=100),
        ),
        migrations.AddField(
            model_name='traitvaluedetails',
            name='recommendations_returnRate',
            field=models.TextField(default='abc', max_length=100),
        ),
    ]
