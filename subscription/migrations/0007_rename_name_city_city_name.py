# Generated by Django 4.2.4 on 2024-02-09 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0006_rename_city_subscription_city_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='name',
            new_name='city_name',
        ),
    ]
