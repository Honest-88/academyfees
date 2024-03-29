# Generated by Django 4.0.5 on 2022-06-28 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_number', models.CharField(default='', max_length=200)),
                ('asset_name', models.CharField(default='', max_length=200)),
                ('asset_value', models.CharField(default='', max_length=200)),
                ('acquired_through', models.CharField(choices=[('Cash', 'Cash'), ('Credit', 'Credit'), ('Donation', 'Donation')], default='Cash', max_length=100)),
                ('date_acqured', models.CharField(default='', max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
