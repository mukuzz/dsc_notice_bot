# Generated by Django 4.0.5 on 2022-06-08 11:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Notices', '0014_notice_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='id',
        ),
        migrations.AlterField(
            model_name='notice',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='notice',
            name='key',
            field=models.CharField(max_length=32, primary_key=True, serialize=False, unique=True),
        ),
    ]
