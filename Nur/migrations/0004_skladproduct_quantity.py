# Generated by Django 4.2.16 on 2024-12-03 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nur', '0003_customuser_last_password_reset'),
    ]

    operations = [
        migrations.AddField(
            model_name='skladproduct',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
