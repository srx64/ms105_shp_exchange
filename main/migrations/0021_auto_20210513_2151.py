# Generated by Django 3.1.7 on 2021-05-13 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210513_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='stock',
        ),
        migrations.AddField(
            model_name='settings',
            name='stock_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='settings',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
