# Generated by Django 5.0.6 on 2024-05-19 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photom', '0022_alter_class_options_alter_schoolaccount_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schoolaccount',
            options={'verbose_name': 'School', 'verbose_name_plural': 'Schools'},
        ),
        migrations.AlterField(
            model_name='class',
            name='class_school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photom.schoolaccount'),
        ),
    ]
