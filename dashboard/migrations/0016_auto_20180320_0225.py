# Generated by Django 2.0.2 on 2018-03-19 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20180320_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traitvaluedetails',
            name='ttid',
        ),
        migrations.AlterField(
            model_name='traitvaluedetails',
            name='sid',
            field=models.OneToOneField(db_column='sid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dashboard.SellerDetails'),
        ),
    ]
