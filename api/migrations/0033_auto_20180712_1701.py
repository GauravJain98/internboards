# Generated by Django 2.0.7 on 2018-07-12 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20180712_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='intern',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='degrees', to='api.Intern'),
        ),
    ]
