# Generated by Django 5.2.1 on 2025-06-11 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='date_reserved',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='reservation',
            name='check_in',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='check_out',
            field=models.DateField(blank=True, null=True),
        ),
    ]
