# Generated by Django 5.1.2 on 2024-10-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_userprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/%Y/%m/%d'),
        ),
    ]
