# Generated by Django 4.0.4 on 2022-06-09 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_userdetail_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]