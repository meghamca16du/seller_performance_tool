# Generated by Django 2.0.2 on 2018-03-28 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0028_auto_20180326_0222'),
        ('feedbacks_app', '0006_auto_20180328_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackDetails',
            fields=[
                ('fid', models.AutoField(primary_key=True, serialize=False)),
                ('feedbackEntered', models.TextField(max_length=300)),
                ('feedbackRating', models.CharField(choices=[('0', 'default'), ('1', 'oneStar'), ('2', 'twoStar'), ('3', 'threeStar'), ('4', 'fourStar'), ('5', 'fiveStar')], default='0', max_length=1)),
                ('dateFeedbackEntered', models.DateField()),
                ('bid', models.ForeignKey(db_column='bid', on_delete=django.db.models.deletion.CASCADE, to='dashboard.BuyerDetails')),
                ('oid', models.ForeignKey(db_column='oid', on_delete=django.db.models.deletion.CASCADE, to='dashboard.OrderDetails')),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='dashboard.ProductDetails')),
            ],
            options={
                'db_table': 'feedback_details',
                'managed': True,
            },
        ),
    ]