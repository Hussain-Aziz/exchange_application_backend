# Generated by Django 4.2.9 on 2024-04-21 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_courseapplication_aus_course_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="courseapplication",
            name="delegated_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.faculty",
            ),
        ),
    ]
