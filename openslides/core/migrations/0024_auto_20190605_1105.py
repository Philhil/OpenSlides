# Generated by Django 2.2.1 on 2019-06-05 09:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0023_chyron_colors")]

    operations = [
        migrations.AlterField(
            model_name="history",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]