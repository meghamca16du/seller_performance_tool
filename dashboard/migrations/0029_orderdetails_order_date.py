# Generated by Django 2.0.2 on 2018-03-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_auto_20180326_0222'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='order_date',
            field=models.DateField(default='2018-03-10'),
        ),
    ]
