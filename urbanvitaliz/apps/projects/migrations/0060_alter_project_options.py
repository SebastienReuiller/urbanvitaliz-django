# Generated by Django 3.2.15 on 2022-09-23 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0059_auto_20220905_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('use_private_notes', 'Can use the private notes'), ('use_public_notes', 'Can use the public notes')), 'verbose_name': 'project', 'verbose_name_plural': 'projects'},
        ),
    ]
