# Generated by Django 3.1.7 on 2021-05-10 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_statistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]