# Generated by Django 3.2.3 on 2021-09-06 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0016_task_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Plus le chiffre est élevé, plus la recommandation s'affichera en haut.",  # noqa
                verbose_name="Priorité",
            ),
        ),
    ]
