# Generated by Django 4.0.4 on 2022-06-08 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_alter_jobdetail_no_of_applicants'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdetail',
            name='Skills',
            field=models.TextField(blank=True, null=True),
        ),
    ]