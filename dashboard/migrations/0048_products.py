# Generated by Django 2.0.2 on 2018-04-21 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0047_auto_20180422_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('product_name', models.TextField(max_length=50)),
                ('subcategory_id', models.TextField(max_length=50)),
                ('product_sale_count', models.IntegerField()),
                ('launch_date', models.DateField()),
                ('score', models.IntegerField()),
                ('inventory', models.IntegerField()),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.SellerDetails')),
            ],
        ),
    ]
