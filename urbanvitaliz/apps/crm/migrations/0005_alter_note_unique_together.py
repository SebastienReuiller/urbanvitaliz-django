# Generated by Django 3.2.15 on 2022-10-04 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0004_note_sticky"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="note",
            unique_together=set(),
        ),
    ]
