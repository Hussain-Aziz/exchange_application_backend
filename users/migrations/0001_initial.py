# Generated by Django 5.0.1 on 2024-02-24 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty_id', models.AutoField(primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=35)),
                ('faculty_name', models.CharField(max_length=30)),
            ],
        ),
    ]