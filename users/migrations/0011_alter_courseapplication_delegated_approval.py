# Generated by Django 4.2.9 on 2024-04-21 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_courseapplication_delegated_approval"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courseapplication",
            name="delegated_approval",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
