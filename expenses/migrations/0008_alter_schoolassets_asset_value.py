# Generated by Django 4.0.5 on 2022-06-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0007_alter_schoolassets_asset_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolassets',
            name='asset_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
