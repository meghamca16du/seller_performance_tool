# Generated by Django 2.0.2 on 2018-04-10 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks_app', '0010_feedbacks_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedbacks_table',
            old_name='rating',
            new_name='rating_points',
        ),
    ]
