# Generated by Django 3.1.6 on 2022-03-24 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_auto_20220324_1355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scoutedmatch',
            old_name='auto_cargo_scored',
            new_name='auto_cargo_scored_high',
        ),
        migrations.AddField(
            model_name='scoutedmatch',
            name='auto_cargo_scored_low',
            field=models.IntegerField(default=0),
        ),
    ]
