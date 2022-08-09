# Generated by Django 3.2.14 on 2022-08-09 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0057_auto_20220801_1717"),
        ("onboarding", "0003_alter_onboardingresponse_onboarding"),
    ]

    operations = [
        migrations.AddField(
            model_name="onboardingresponse",
            name="project",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="onboarding",
                to="projects.project",
            ),
            preserve_default=False,
        ),
    ]
