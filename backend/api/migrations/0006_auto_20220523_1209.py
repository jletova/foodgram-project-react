# Generated by Django 2.2.16 on 2022-05-23 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20220519_0253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['-id']},
        ),
    ]