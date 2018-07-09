# Generated by Django 2.0.6 on 2018-07-09 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20180709_0646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='college',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='company_user',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='custom_user',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='degree',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='github',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='intern',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='internship',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='siteadmin',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='skill',
            old_name='delete',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='delete',
            new_name='archived',
        ),
    ]
