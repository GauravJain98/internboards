# Generated by Django 2.0.6 on 2018-07-05 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0002_auto_20180703_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='oauth.Client', verbose_name='User'),
        ),
    ]
