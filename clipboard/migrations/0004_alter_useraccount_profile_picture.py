# Generated by Django 3.2.4 on 2021-07-02 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clipboard", "0003_useraccount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="profile_picture",
            field=models.ImageField(
                blank=True, default="default.png", null=True, upload_to=""
            ),
        ),
    ]
