# Generated by Django 4.0.4 on 2024-04-15 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photom', '0010_remove_student_student_photo_id_b_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_photos',
        ),
        migrations.AlterField(
            model_name='student',
            name='student_photo_ID',
            field=models.ImageField(default='photo-ids/default-photo-id.PNG', upload_to='photo-ids'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='student-pictures')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('school_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photom.schoolaccount')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photom.student')),
            ],
        ),
    ]
