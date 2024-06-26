# Generated by Django 4.2.10 on 2024-04-01 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whistleblower', '0005_alter_complaint_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='complaint_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'New'), (2, 'In Progress'), (3, 'Resolved')], default=1),
        ),
    ]
