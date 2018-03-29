# Generated by Django 2.0.2 on 2018-03-28 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks_app', '0004_auto_20180328_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackdetails',
            name='feedbackRating',
            field=models.IntegerField(choices=[(0, 'default'), (1, 'oneStar'), (2, 'twoStar'), (3, 'threeStar'), (4, 'fourStar'), (5, 'fiveStar')], default=0),
        ),
    ]