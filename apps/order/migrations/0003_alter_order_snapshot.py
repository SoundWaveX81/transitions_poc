# Generated by Django 5.2 on 2025-04-14 23:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0002_alter_order_snapshot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="snapshot",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
