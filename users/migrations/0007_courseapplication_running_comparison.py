# Generated by Django 4.2.9 on 2024-04-18 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_courseapplication_comparison_result_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="courseapplication",
            name="running_comparison",
            field=models.BooleanField(default=False),
        ),
    ]
