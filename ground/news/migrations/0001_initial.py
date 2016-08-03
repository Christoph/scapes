# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-03 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.BigIntegerField()),
                ('text', models.CharField(max_length=250)),
                ('truncated', models.BooleanField(default=False)),
                ('lang', models.CharField(blank=True, default=None, max_length=9, null=True)),
                ('user_id', models.BigIntegerField()),
                ('user_screen_name', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=150)),
                ('user_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(db_index=True)),
                ('user_utc_offset', models.IntegerField(blank=True, default=None, null=True)),
                ('user_time_zone', models.CharField(blank=True, default=None, max_length=150, null=True)),
                ('filter_level', models.CharField(blank=True, default=None, max_length=6, null=True)),
                ('latitude', models.FloatField(blank=True, default=None, null=True)),
                ('longitude', models.FloatField(blank=True, default=None, null=True)),
                ('user_geo_enabled', models.BooleanField(default=False)),
                ('user_location', models.CharField(blank=True, default=None, max_length=150, null=True)),
                ('favorite_count', models.PositiveIntegerField(blank=True, null=True)),
                ('retweet_count', models.PositiveIntegerField(blank=True, null=True)),
                ('user_followers_count', models.PositiveIntegerField(blank=True, null=True)),
                ('user_friends_count', models.PositiveIntegerField(blank=True, null=True)),
                ('in_reply_to_status_id', models.BigIntegerField(blank=True, default=None, null=True)),
                ('retweeted_status_id', models.BigIntegerField(blank=True, default=None, null=True)),
            ],
        ),
    ]
