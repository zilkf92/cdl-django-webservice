# Generated by Django 3.1.13 on 2021-12-07 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdl_rest_api', '0007_auto_20211206_1006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clusterstate',
            old_name='numberOfQubits',
            new_name='amountQubits',
        ),
        migrations.RenameField(
            model_name='clusterstate',
            old_name='graphState',
            new_name='presetSettings',
        ),
    ]
