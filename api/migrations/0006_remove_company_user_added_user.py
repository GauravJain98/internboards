# Generated by Django 2.0.6 on 2018-06-25 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180625_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_user',
            name='added_user',
        ),
    ]