# Generated by Django 4.0.4 on 2024-04-14 16:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photom', '0008_alter_student_student_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_photo_ID',
            field=models.ImageField(upload_to='photo-ids'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_photos',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=[], null=True, size=None),
        ),
    ]
