# Generated by Django 4.1.7 on 2023-05-23 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_complaint_escalation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.IntegerField(choices=[(1, 'Solved'), (2, 'InProgress'), (3, 'Pending'), (4, 'Escalated')], default=3),
        ),
    ]