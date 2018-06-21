# Generated by Django 2.0.6 on 2018-06-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180621_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='internship',
            old_name='application_number',
            new_name='applications',
        ),
        migrations.RenameField(
            model_name='internship',
            old_name='responsibility',
            new_name='responsibilities',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='interns_applied',
        ),
        migrations.RemoveField(
            model_name='internshipavailable',
            name='sub',
        ),
        migrations.RemoveField(
            model_name='siteadmin',
            name='sub',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='sub',
        ),
        migrations.AddField(
            model_name='internshipavailable',
            name='college',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteadmin',
            name='college',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='college',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='hiring',
            name='college',
            field=models.CharField(max_length=20),
        ),
    ]
