# Generated by Django 4.0.4 on 2022-06-07 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_jobdetail_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdetail',
            name='about_company',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobdetail',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='jobdetail',
            name='no_of_applicants',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobdetail',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]