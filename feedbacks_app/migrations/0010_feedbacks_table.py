# Generated by Django 2.0.2 on 2018-04-10 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_auto_20180403_1432'),
        ('feedbacks_app', '0009_auto_20180410_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedbacks_table',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('feedback_date', models.DateField()),
                ('rating', models.IntegerField()),
                ('feedback', models.TextField(max_length=500)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ProductMain')),
            ],
        ),
    ]