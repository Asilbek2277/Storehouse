# Generated by Django 5.0.3 on 2024-03-09 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0003_tarqatuvchi_qarz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarqatuvchi',
            name='qarz',
        ),
    ]