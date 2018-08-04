# Generated by Django 2.0.7 on 2018-07-21 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_submission_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='api.Sub'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='available',
            field=models.ManyToManyField(related_name='internships', to='api.Sub'),
        ),
    ]
