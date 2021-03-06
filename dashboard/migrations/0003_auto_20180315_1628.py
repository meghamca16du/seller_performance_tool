# Generated by Django 2.0.2 on 2018-03-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20180315_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='status',
            field=models.CharField(choices=[('OD', 'ontime_delivery'), ('LD', 'late_delivery'), ('C', 'cancelled'), ('R', 'returned'), ('IP', 'in_process'), ('D', 'dispatched')], default='IP', max_length=2),
        ),
    ]
