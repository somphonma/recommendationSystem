# Generated by Django 3.1.7 on 2021-03-04 09:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyAPI', '0002_auto_20210304_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvals',
            name='gpa_high_school',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(4.0)]),
        ),
    ]
