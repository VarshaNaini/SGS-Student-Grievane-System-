# Generated by Django 4.1.7 on 2023-04-03 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_complaint_timer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='To',
            field=models.CharField(choices=[('CIVIL_HOD', 'CIVIL HOD'), ('CSE_HOD', 'CSE HOD'), ('ECE_HOD', 'ECE HOD'), ('ECM_HOD', 'ECM HOD'), ('EEE_HOD', 'EEE HOD'), ('IT_HOD', 'IT HOD'), ('MECH HOD', 'MECH HOD'), ('MBA HOD', 'MBA HOD'), ('MANAGEMENT', 'MANAGEMENT'), ('PRINCIPLE', 'PRINCIPLE'), ('DIRECTOR', 'DIRECTOR'), ('CEO', 'CEO')], max_length=200, null=True),
        ),
    ]
