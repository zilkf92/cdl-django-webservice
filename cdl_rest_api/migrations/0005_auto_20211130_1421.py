# Generated by Django 3.1.13 on 2021-11-30 14:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cdl_rest_api', '0004_auto_20211130_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
