# Generated by Django 3.2 on 2021-04-23 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="date updated")),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="date updated")),
                ("first_name", models.CharField(blank=True, max_length=255, null=True)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "profile_picture",
                    models.ImageField(default="app/templates/misc/default_profile_picture.png", upload_to=""),
                ),
                ("profile_picture_name", models.CharField(blank=True, max_length=50, null=True)),
                ("email_address", models.EmailField(max_length=254, unique=True)),
                ("phone_number", models.CharField(blank=True, max_length=20, null=True)),
                ("room_number", models.CharField(blank=True, max_length=10, null=True)),
                ("subjects_taught", models.ManyToManyField(blank=True, to="app.Subject")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
