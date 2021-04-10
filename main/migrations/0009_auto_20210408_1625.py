# Generated by Django 3.1.7 on 2021-04-08 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_images'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Images',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='avatars/'),
        ),
    ]