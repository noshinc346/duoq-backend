# Generated by Django 5.0.4 on 2024-04-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesinterested',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gamesplayed',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gamesplaying',
            name='game',
        ),
        migrations.AddField(
            model_name='games',
            name='gamesInterested',
            field=models.ManyToManyField(to='games_app.gamesinterested'),
        ),
        migrations.AddField(
            model_name='games',
            name='gamesPlayed',
            field=models.ManyToManyField(to='games_app.gamesplayed'),
        ),
        migrations.AddField(
            model_name='games',
            name='gamesPlaying',
            field=models.ManyToManyField(to='games_app.gamesplaying'),
        ),
    ]
