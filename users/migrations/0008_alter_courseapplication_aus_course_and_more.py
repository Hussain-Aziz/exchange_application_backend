# Generated by Django 4.2.9 on 2024-04-21 18:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_courseapplication_running_comparison"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courseapplication",
            name="aus_course",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="courseapplication",
            name="aus_syllabus",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="courseapplication",
            name="course_code",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="courseapplication",
            name="course_title",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="courseapplication",
            name="grade_required",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="courseapplication",
            name="program_area",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="courseapplication",
            name="syllabus",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="aus_id",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="current_standing",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="expected_graduation",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="host_contact_email",
            field=models.EmailField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="host_contact_name",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="name",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="present_college",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="present_major",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="university",
            name="university_name",
            field=models.CharField(blank=True, max_length=250),
        ),
    ]