# Generated by Django 4.1.1 on 2022-09-27 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_alter_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
    ]
