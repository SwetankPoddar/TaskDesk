# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-11 19:57
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=25)),
                ('categoryImage', models.ImageField(blank=True, upload_to=b'media')),
                ('created_at', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateTimeField()),
                ('personal_due_date', models.DateTimeField()),
                ('task_name', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(editable=False)),
                ('modifed_at', models.DateTimeField()),
                ('priority_level', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskdesk.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, upload_to=b'profile_images')),
                ('high_priority_color', models.CharField(default=b'FF0000', max_length=6)),
                ('medium_priority_color', models.CharField(default=b'FFA500', max_length=6)),
                ('low_priority_color', models.CharField(default=b'00FF00', max_length=6)),
                ('color_mode', models.CharField(default=b'D', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tasks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskdesk.UserProfile'),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskdesk.UserProfile'),
        ),
    ]