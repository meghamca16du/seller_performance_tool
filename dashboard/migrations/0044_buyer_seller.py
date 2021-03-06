# Generated by Django 2.0.2 on 2018-04-21 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0043_auto_20180417_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('bname', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'Buyer',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('sname', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'Seller',
                'managed': True,
            },
        ),
    ]
