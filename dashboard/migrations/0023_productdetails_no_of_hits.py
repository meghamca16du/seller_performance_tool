# Generated by Django 2.0.2 on 2018-03-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_traitvaluedetails_overall_perf_val'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetails',
            name='no_of_hits',
            field=models.CharField(default=0, max_length=5),
        ),
    ]
