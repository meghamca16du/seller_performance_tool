# Generated by Django 2.0.2 on 2018-03-15 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='status',
            field=models.CharField(choices=[('OD', 'ontime_delivery'), ('LD', 'late_delivery'), ('R', 'returned'), ('IP', 'in_process'), ('D', 'dispatched')], default='IP', max_length=2),
        ),
    ]
