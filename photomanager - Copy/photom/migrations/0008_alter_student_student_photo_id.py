# Generated by Django 4.0.4 on 2024-04-14 15:43

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photom', '0007_alter_student_student_photo_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_photo_ID',
            field=models.ImageField(default='https://adonisrecycling.com/wp-content/uploads/2021/06/male-placeholder.jpeg', storage=django.core.files.storage.FileSystemStorage(location='/media/photo-ids'), upload_to=''),
        ),
    ]
