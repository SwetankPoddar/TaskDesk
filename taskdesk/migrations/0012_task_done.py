# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-13 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskdesk', '0011_auto_20190313_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
