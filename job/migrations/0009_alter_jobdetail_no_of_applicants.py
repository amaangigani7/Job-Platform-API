# Generated by Django 4.0.4 on 2022-06-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_remove_jobdetail_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdetail',
            name='no_of_applicants',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
