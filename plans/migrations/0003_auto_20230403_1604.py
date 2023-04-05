# Generated by Django 3.2 on 2023-04-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_challenge_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='likes_challenge',
        ),
        migrations.AddField(
            model_name='challenge',
            name='intro',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='outro',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='steps',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='tips',
            field=models.TextField(blank=True),
        ),
    ]