# Generated by Django 4.0.4 on 2022-06-06 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='recruiter',
            field=models.BooleanField(default=False),
        ),
    ]
