# Generated by Django 5.0.4 on 2024-04-11 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_alter_preference_female_alter_preference_male_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
