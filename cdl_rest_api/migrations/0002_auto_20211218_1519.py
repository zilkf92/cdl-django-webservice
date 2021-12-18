# Generated by Django 3.1.13 on 2021-12-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdl_rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='status',
            field=models.CharField(blank=True, choices=[('INITIAL', 'Initial'), ('IN QUEUE', 'In Queue'), ('RUNNING', 'Running'), ('FAILED', 'Failed'), ('DONE', 'Done')], max_length=255, null=True),
        ),
    ]
