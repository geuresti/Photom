# Generated by Django 4.0.4 on 2024-03-31 21:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photom', '0004_alter_student_student_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_photos',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(blank=True, default='https://adonisrecycling.com/wp-content/uploads/2021/06/male-placeholder.jpeg', upload_to=''), default=[], size=None),
        ),
    ]
