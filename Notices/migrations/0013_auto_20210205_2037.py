# Generated by Django 2.2.13 on 2021-02-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notices', '0012_notice_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='notice',
            name='url',
            field=models.CharField(max_length=1024),
        ),
    ]
