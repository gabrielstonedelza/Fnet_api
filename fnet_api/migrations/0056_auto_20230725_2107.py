# Generated by Django 3.2.9 on 2023-07-25 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0055_commercials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commercials',
            name='calbank_youtube_video_link',
        ),
        migrations.RemoveField(
            model_name='commercials',
            name='fidelity_youtube_video_link',
        ),
        migrations.RemoveField(
            model_name='commercials',
            name='mtn_youtube_video_link',
        ),
    ]