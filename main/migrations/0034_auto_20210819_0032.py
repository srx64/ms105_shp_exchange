# Generated by Django 3.1.7 on 2021-08-18 21:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_order_is_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]