# Generated by Django 2.0.6 on 2018-07-05 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_internship_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internship',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
