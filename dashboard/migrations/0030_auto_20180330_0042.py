# Generated by Django 2.0.2 on 2018-03-29 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_orderdetails_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='traitvaluedetails',
            name='recommendations_returnRate',
            field=models.TextField(default='abc', max_length=100),
        ),
        migrations.AddField(
            model_name='traitvaluedetails',
            name='return_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
