# Generated by Django 5.0.4 on 2024-04-12 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games_app', '0006_rename_game_usergame_game_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usergame',
            old_name='game_id',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='usergame',
            old_name='profile_id',
            new_name='profile',
        ),
    ]
