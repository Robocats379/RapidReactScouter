# Generated by Django 3.1.6 on 2022-03-25 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20220324_1328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('team_number',)},
        ),
    ]
