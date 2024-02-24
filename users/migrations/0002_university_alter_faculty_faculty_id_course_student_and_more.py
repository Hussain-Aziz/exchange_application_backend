# Generated by Django 5.0.1 on 2024-02-24 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('university_id', models.IntegerField(primary_key=True, serialize=False)),
                ('university_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='faculty',
            name='faculty_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.IntegerField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=20)),
                ('facultyid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_num', models.IntegerField()),
                ('expected_graduation', models.CharField(max_length=15)),
                ('universityid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.university')),
            ],
        ),
        migrations.CreateModel(
            name='CourseApplication',
            fields=[
                ('course_application_id', models.AutoField(primary_key=True, serialize=False)),
                ('semester', models.CharField(max_length=15)),
                ('grade', models.CharField(max_length=2)),
                ('courseid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.course')),
                ('facultyid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.faculty')),
                ('studentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
                ('universityid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.university')),
            ],
        ),
    ]
