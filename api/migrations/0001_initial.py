# Generated by Django 4.1.12 on 2023-10-19 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HbAppEntity",
            fields=[
                (
                    "_id",
                    models.CharField(
                        editable=False, max_length=24, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("entityCode", models.UUIDField()),
                ("description", models.TextField()),
                ("applicationCode", models.CharField(max_length=10)),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "hb_app_entities",
            },
        ),
    ]
