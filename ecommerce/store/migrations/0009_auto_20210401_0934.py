# Generated by Django 3.1.7 on 2021-04-01 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='date_comments',
            new_name='date_commented',
        ),
    ]
