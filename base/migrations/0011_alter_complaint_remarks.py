# Generated by Django 4.1.7 on 2023-04-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_complaint_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='remarks',
            field=models.TextField(max_length=4000, null=True),
        ),
    ]
