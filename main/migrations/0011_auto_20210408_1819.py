# Generated by Django 3.1.7 on 2021-04-08 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20210408_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='avatars/'),
        ),
    ]