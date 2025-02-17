# Generated by Django 3.2.13 on 2022-05-23 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("home", "0005_siteconfiguration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteconfiguration",
            name="site",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="sites.site"
            ),
        ),
    ]
