# Generated by Django 4.2.16 on 2024-12-03 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nur', '0009_client_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]