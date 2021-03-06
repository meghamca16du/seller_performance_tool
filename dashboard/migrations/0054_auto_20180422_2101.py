# Generated by Django 2.0.2 on 2018-04-22 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0053_auto_20180422_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('oid', models.CharField(max_length=7)),
                ('status', models.CharField(choices=[('OD', 'ontime_delivery'), ('LD', 'late_delivery'), ('C', 'cancelled'), ('R', 'returned'), ('IP', 'in_process'), ('D', 'dispatched')], default='IP', max_length=2)),
                ('order_date', models.DateField()),
                ('exp_shipment', models.DateField()),
                ('exp_delivery', models.DateField()),
                ('actual_shipment', models.DateField(blank=True, null=True)),
                ('actual_delivery', models.DateField(blank=True, null=True)),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Buyer')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Products')),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Seller')),
            ],
            options={
                'db_table': 'details_of_orders',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='orders',
            unique_together={('oid', 'product_id', 'seller_id', 'buyer_id')},
        ),
    ]
