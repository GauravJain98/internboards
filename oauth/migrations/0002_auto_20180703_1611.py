# Generated by Django 2.0.6 on 2018-07-03 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='expires',
            field=models.IntegerField(default=1800),
        ),
    ]