# Generated by Django 4.0.5 on 2022-06-28 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='term',
            new_name='month',
        ),
    ]
