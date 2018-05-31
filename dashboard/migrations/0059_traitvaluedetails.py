# Generated by Django 2.0.2 on 2018-04-22 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0058_auto_20180423_0209'),
    ]

    operations = [
        migrations.CreateModel(
            name='TraitValueDetails',
            fields=[
                ('tid', models.TextField(primary_key=True, serialize=False)),
                ('overall_perf_val', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('late_shipment_rate', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('recommendations_lateShipmentRate', models.TextField(max_length=100)),
                ('on_time_delivery', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('recommendations_onTimeDeliery', models.TextField(max_length=100)),
                ('hit_to_success_ratio', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('recommendations_HitToSucessRatio', models.TextField(max_length=100)),
                ('return_rate', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('recommendations_returnRate', models.TextField(max_length=100)),
                ('positive_feedbacks', models.TextField(max_length=500)),
                ('negative_feedbacks', models.TextField(max_length=500)),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Seller')),
            ],
            options={
                'db_table': 'traits_value_details',
                'managed': True,
            },
        ),
    ]