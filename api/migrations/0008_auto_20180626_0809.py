# Generated by Django 2.0.6 on 2018-06-26 08:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_company_user_added_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='internship',
            old_name='catagory',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='company_user',
            name='added_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='end',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='degree',
            name='start',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='job',
            name='end',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='job',
            name='start',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='project',
            name='end',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='project',
            name='start',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
