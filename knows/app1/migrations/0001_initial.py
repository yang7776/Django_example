# Generated by Django 2.1.5 on 2019-01-21 10:28

import app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('selfid', models.CharField(max_length=77, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=77)),
                ('photo', models.ImageField(blank=True, upload_to=app1.models.user_directory_path)),
            ],
        ),
    ]
