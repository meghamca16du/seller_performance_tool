# Generated by Django 2.0.2 on 2018-03-19 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_traitvaluedetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traitvaluedetails',
            name='sid',
            field=models.ForeignKey(db_column='sid', on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.SellerDetails', unique=True),
        ),
    ]