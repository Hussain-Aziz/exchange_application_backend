# Generated by Django 4.2.9 on 2024-05-01 13:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_student_form_comments"),
    ]

    operations = [
        migrations.AddField(
            model_name="courseapplication",
            name="ignore_aus_syllabus",
            field=models.BooleanField(default=False),
        ),
    ]
