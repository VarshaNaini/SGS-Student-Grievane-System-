# Generated by Django 4.1.7 on 2023-04-08 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_complaint_current_handler'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='escalation_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]