# Generated by Django 4.1.7 on 2023-04-03 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_delete_countdown_complaint_timer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='timer',
        ),
    ]
