# Generated by Django 4.2.9 on 2024-04-15 21:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_remove_student_student_id_student_aus_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="courseapplication",
            name="department",
            field=models.IntegerField(
                choices=[
                    (0, "Architecture"),
                    (1, "Art and Design"),
                    (2, "Arabic and Translation Studies"),
                    (3, "Biology, Chemistry and Environmental Sciences"),
                    (4, "English"),
                    (5, "International Studies"),
                    (6, "Media Communication"),
                    (7, "Mathematics and Statistics"),
                    (8, "Physics"),
                    (9, "Psychology"),
                    (10, "Chemical and Biological Engineering"),
                    (11, "Civil Engineering"),
                    (12, "Computer Science and Engineering"),
                    (13, "Electrical Engineering"),
                    (14, "Industrial Engineering"),
                    (15, "Mechanical Engineering"),
                    (16, "Accounting"),
                    (17, "Economics"),
                    (18, "Finance"),
                    (19, "Management, Strategy and Entrepreneurship"),
                    (20, "Marketing and Information Systems"),
                ],
                default=0,
            ),
        ),
    ]